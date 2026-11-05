import ipaddress
import socket
from urllib.parse import urlparse


BLOCKED_HOSTNAMES = {
    "localhost",
    "localhost.localdomain",
    "ip6-localhost",
    "ip6-loopback",
}


def is_private_or_reserved_ip(ip: str) -> bool:
    """
    Return True if an IP is not globally routable.
    This blocks private, loopback, link-local, multicast,
    reserved and unspecified IP addresses.
    """

    try:
        address = ipaddress.ip_address(ip)
        return not address.is_global

    except ValueError:
        return True


def validate_public_url(url: str) -> tuple[bool, str]:
    """
    Validate HTTP/HTTPS URLs and ensure their hostnames
    resolve exclusively to globally routable IP addresses.

    Returns:
        (True, "") when safe
        (False, reason) when blocked
    """

    try:
        parsed = urlparse(url)

        # Allow only HTTP and HTTPS
        if parsed.scheme.lower() not in {"http", "https"}:
            return False, "Only HTTP and HTTPS URLs are allowed"

        hostname = parsed.hostname

        if not hostname:
            return False, "URL does not contain a valid hostname"

        hostname = hostname.lower().rstrip(".")

        # Block localhost hostnames
        if (
            hostname in BLOCKED_HOSTNAMES
            or hostname.endswith(".localhost")
        ):
            return False, "Localhost access is not allowed"

        # Validate port
        try:
            port = parsed.port

        except ValueError:
            return False, "Invalid URL port"

        # ------------------------------------------------
        # DIRECT IP ADDRESS VALIDATION
        # ------------------------------------------------

        try:
            address = ipaddress.ip_address(hostname)

            if not address.is_global:
                return False, (
                    "Private or reserved IP addresses are not allowed"
                )

            return True, ""

        except ValueError:
            # Not an IP address. Continue with DNS resolution.
            pass

        # ------------------------------------------------
        # DOMAIN DNS RESOLUTION
        # ------------------------------------------------

        try:
            addresses = socket.getaddrinfo(
                hostname,
                port or 443 if parsed.scheme.lower() == "https" else port or 80,
                type=socket.SOCK_STREAM
            )

        except socket.gaierror:
            return False, "Unable to resolve hostname"

        if not addresses:
            return False, "Hostname did not resolve"

        resolved_ips = {
            result[4][0]
            for result in addresses
            if result[4]
        }

        if not resolved_ips:
            return False, "Hostname did not resolve to an IP address"

        # Every resolved address must be globally routable.
        for ip in resolved_ips:

            if is_private_or_reserved_ip(ip):
                return (
                    False,
                    "Hostname resolves to a private or reserved IP address"
                )

        return True, ""

    except Exception as exc:

        return False, f"URL validation failed: {exc}"


def normalize_url(url: str) -> str:
    """
    Normalize URLs for comparison.

    Examples:
        https://google.com
        https://google.com/

    Both are treated as equivalent.
    """

    try:
        parsed = urlparse(url)

        scheme = parsed.scheme.lower()
        hostname = (parsed.hostname or "").lower().rstrip(".")

        if ":" in hostname:
            hostname = f"[{hostname}]"

        port = parsed.port

        if port is None or (
            (scheme == "http" and port == 80)
            or
            (scheme == "https" and port == 443)
        ):
            netloc = hostname

        else:
            netloc = f"{hostname}:{port}"

        path = parsed.path or "/"

        if path != "/" and path.endswith("/"):
            path = path.rstrip("/")

        return (
            f"{scheme}://"
            f"{netloc}"
            f"{path}"
            f"{('?' + parsed.query) if parsed.query else ''}"
            f"{('#' + parsed.fragment) if parsed.fragment else ''}"
        )

    except Exception:
        return url.rstrip("/")