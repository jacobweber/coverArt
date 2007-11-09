#!/usr/bin/python

import BaseHTTPServer, urllib, cgi, urlparse, pprint, albumDatabase, amazonCoverArt, stpy, md5

albumDB = None

class CoverArtServer(BaseHTTPServer.BaseHTTPRequestHandler):
	SERVER_PORT = 80

	VALID_TYPES = ('image/jpeg','image/gif')

	INIT_SESSION_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
	<plist version="1.0">
		<dict>
			<key>signature</key>
			<data>eCaO0TnK/2u3x6i5pCcS+fDXHoKVNw4oj7TsNNanqKRsbqfUWDf7PDUMRWsCYiCLuF8lAgurKQKs5tHS05YdVq9+s6zptCYRnJfPLlJGh8ezzjP3mp3X4ReiCz1ig23OyrF2iXgz3Bd3LBd4USbhh8IoXQsNBwJPXYaM6nrHgH8=</data>
			<key>certs</key>
			<array>
<data>MIIFbzCCBNigAwIBAgIERpxLpjANBgkqhkiG9w0BAQUFADCBwzELMAkGA1UEBhMCVVMxFDASBgNVBAoTC0VudHJ1c3QubmV0MTswOQYDVQQLEzJ3d3cuZW50cnVzdC5uZXQvQ1BTIGluY29ycC4gYnkgcmVmLiAobGltaXRzIGxpYWIuKTElMCMGA1UECxMcKGMpIDE5OTkgRW50cnVzdC5uZXQgTGltaXRlZDE6MDgGA1UEAxMxRW50cnVzdC5uZXQgU2VjdXJlIFNlcnZlciBDZXJ0aWZpY2F0aW9uIEF1dGhvcml0eTAeFw0wNzA4MzAxNzQ3MjNaFw0wODA5MzAxODE3MjJaMIGNMQswCQYDVQQGEwJVUzETMBEGA1UECBMKQ2FsaWZvcm5pYTESMBAGA1UEBxMJQ3VwZXJ0aW5vMRIwEAYDVQQKEwlBcHBsZSBJbmMxGDAWBgNVBAsTD2lUdW5lcyBTdG9yZSBRQTEnMCUGA1UEAxMeaVR1bmVzLVN0b3JlLVVSTC1CYWcuYXBwbGUuY29tMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCghE1fwL7LQW1KfwEK97xgUTV+HNfuV8CHApTKcBB0jtuKgSIPUFDwJvGVSD0ZVe4OK8Hn/oiuXuUvLeaL9TqZhk4z2fOCK76eJpy6T/Q1xSiw2rAlFv5g+n8SIG3nCM2UVA+g6JMJtgiqjV3MKgm2CjojDM2+df+IPxjhOn9EoQIDAQABo4ICojCCAp4wCwYDVR0PBAQDAgWgMCsGA1UdEAQkMCKADzIwMDcwODMwMTc0NzIzWoEPMjAwODA5MzAxODE3MjJaMBEGCWCGSAGG+EIBAQQEAwIGQDATBgNVHSUEDDAKBggrBgEFBQcDATCCAWgGA1UdIASCAV8wggFbMIIBVwYJKoZIhvZ9B0sCMIIBSDAmBggrBgEFBQcCARYaaHR0cDovL3d3dy5
lbnRydXN0Lm5ldC9jcHMwggEcBggrBgEFBQcCAjCCAQ4aggEKVGhlIEVudHJ1c3QgU1NMIFdlYiBTZXJ2ZXIgQ2VydGlmaWNhdGlvbiBQcmFjdGljZSBTdGF0ZW1lbnQgKENQUykgYXZhaWxhYmxlIGF0IHd3dy5lbnRydXN0Lm5ldC9jcHMgIGlzIGhlcmVieSBpbmNvcnBvcmF0ZWQgaW50byB5b3VyIHVzZSBvciByZWxpYW5jZSBvbiB0aGlzIENlcnRpZmljYXRlLiAgVGhpcyBDUFMgY29udGFpbnMgbGltaXRhdGlvbnMgb24gd2FycmFudGllcyBhbmQgbGlhYmlsaXRpZXMuIENvcHlyaWdodCAoYykgMjAwMiBFbnRydXN0IExpbWl0ZWQwMwYDVR0fBCwwKjAooCagJIYiaHR0cDovL2NybC5lbnRydXN0Lm5ldC9zZXJ2ZXIxLmNybDAzBggrBgEFBQcBAQQnMCUwIwYIKwYBBQUHMAGGF2h0dHA6Ly9vY3NwLmVudHJ1c3QubmV0MB8GA1UdIwQYMBaAFPAXYhNVPbP/CgBr+1CEl/PtYtAaMB0GA1UdDgQWBBTfjeXOmHKQZ9C6bvMXAHXfBZ+PnzAJBgNVHRMEAjAAMBkGCSqGSIb2fQdBAAQMMAobBFY3LjEDAgMoMA0GCSqGSIb3DQEBBQUAA4GBAClHENO5CjG5xrsVaWBymw/Sh9nE/7HzB1NfxXbC9aQMrNCrdv+L1dfr+RsJGNtEnR36j+D52sGF3gxwgU4V2zhH/3AKFlly9Eb911yQp5ELCU54vIosrj599Q74BTeKxQnK671dQCk+LCbr6/ggFXpTLdWm7VqJXNOw0gGeCrNM</data>
			</array>
			<key>bag</key>
<data>PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjwhRE9DVFlQRSBwbGlzdCBQVUJMSUMgIi0vL0FwcGxlIENvbXB1dGVyLy9EVEQgUExJU1QgMS4wLy9FTiIgImh0dHA6Ly93d3cuYXBwbGUuY29tL0RURHMvUHJvcGVydHlMaXN0LTEuMC5kdGQiPiAKCiAgPHBsaXN0IHZlcnNpb249IjEuMCI+CiAgICA8ZGljdD4KICAgICAgCiAgICAgIAogICAgICAKICAgICAgCiAgICAgICAgPGtleT5zdG9yZUZyb250PC9rZXk+PHN0cmluZz5odHRwOi8vYXgucGhvYm9zLmFwcGxlLmNvbS5lZGdlc3VpdGUubmV0L1dlYk9iamVjdHMvTVpTdG9yZS53b2Evd2Evc3RvcmVGcm9udDwvc3RyaW5nPgogICAgPGtleT5uZXdVc2VyU3RvcmVGcm9udDwva2V5PjxzdHJpbmc+aHR0cDovL3Bob2Jvcy5hcHBsZS5jb20vV2ViT2JqZWN0cy9NWlN0b3JlLndvYS93YS9maXJzdExhdW5jaDwvc3RyaW5nPgogICAgPGtleT5uZXdJUG9kVXNlclN0b3JlRnJvbnQ8L2tleT48c3RyaW5nPmh0dHA6Ly9heC5waG9ib3MuYXBwbGUuY29tLmVkZ2VzdWl0ZS5uZXQvV2ViT2JqZWN0cy9NWlN0b3JlLndvYS93YS9uZXdJUG9kVXNlcj9uZXdJUG9kVXNlcj10cnVlPC9zdHJpbmc+CiAgICA8a2V5Pm5ld1Bob25lVXNlcjwva2V5PjxzdHJpbmc+aHR0cDovL2F4LnBob2Jvcy5hcHBsZS5jb20uZWRnZXN1aXRlLm5ldC9XZWJPYmplY3RzL01aU3RvcmUud29hL3dhL3Bob25lTGFuZGluZ1BhZ2U8L3N
0cmluZz4gICAgICAgICAgICAgICAgICAKICAgIDxrZXk+c2VhcmNoPC9rZXk+PHN0cmluZz5odHRwOi8vYXgucGhvYm9zLmFwcGxlLmNvbS5lZGdlc3VpdGUubmV0L1dlYk9iamVjdHMvTVpTZWFyY2gud29hL3dhL3NlYXJjaDwvc3RyaW5nPgogICAgPGtleT5hZHZhbmNlZFNlYXJjaDwva2V5PjxzdHJpbmc+aHR0cDovL2F4LnBob2Jvcy5hcHBsZS5jb20uZWRnZXN1aXRlLm5ldC9XZWJPYmplY3RzL01aU2VhcmNoLndvYS93YS9hZHZhbmNlZFNlYXJjaDwvc3RyaW5nPgogICAgPGtleT5zZWFyY2hIaW50czwva2V5PjxzdHJpbmc+aHR0cDovL2F4LnBob2Jvcy5hcHBsZS5jb20uZWRnZXN1aXRlLm5ldC9XZWJPYmplY3RzL01aU2VhcmNoSGludHMud29hL3dhL2hpbnRzPC9zdHJpbmc+CiAgICA8a2V5PnBhcmVudGFsQWR2aXNvcnk8L2tleT48c3RyaW5nPmh0dHA6Ly9heC5waG9ib3MuYXBwbGUuY29tLmVkZ2VzdWl0ZS5uZXQvV2ViT2JqZWN0cy9NWlN0b3JlLndvYS93YS9wYXJlbnRhbEFkdmlzb3J5PC9zdHJpbmc+CiAgICA8a2V5PnNvbmdNZXRhRGF0YTwva2V5PjxzdHJpbmc+aHR0cDovL2F4LnBob2Jvcy5hcHBsZS5jb20uZWRnZXN1aXRlLm5ldC9XZWJPYmplY3RzL01aU3RvcmUud29hL3dhL3NvbmdNZXRhRGF0YTwvc3RyaW5nPgogICAgPGtleT5icm93c2U8L2tleT48c3RyaW5nPmh0dHA6Ly9heC5waG9ib3MuYXBwbGUuY29tLmVkZ2VzdWl0ZS5uZXQvV2ViT2JqZWN0cy9NWlN0b3JlLndvYS93YS9ic
m93c2U8L3N0cmluZz4KICAgIDxrZXk+YnJvd3NlU3RvcmU8L2tleT48c3RyaW5nPmh0dHA6Ly9heC5waG9ib3MuYXBwbGUuY29tLmVkZ2VzdWl0ZS5uZXQvV2ViT2JqZWN0cy9NWlN0b3JlLndvYS93YS9icm93c2VTdG9yZTwvc3RyaW5nPgogICAgPGtleT5icm93c2VHZW5yZTwva2V5PjxzdHJpbmc+aHR0cDovL2F4LnBob2Jvcy5hcHBsZS5jb20uZWRnZXN1aXRlLm5ldC9XZWJPYmplY3RzL01aU3RvcmUud29hL3dhL2Jyb3dzZUdlbnJlPC9zdHJpbmc+CiAgICA8a2V5PmJyb3dzZUFydGlzdDwva2V5PjxzdHJpbmc+aHR0cDovL2F4LnBob2Jvcy5hcHBsZS5jb20uZWRnZXN1aXRlLm5ldC9XZWJPYmplY3RzL01aU3RvcmUud29hL3dhL2Jyb3dzZUFydGlzdDwvc3RyaW5nPgogICAgPGtleT5icm93c2VBbGJ1bTwva2V5PjxzdHJpbmc+aHR0cDovL2F4LnBob2Jvcy5hcHBsZS5jb20uZWRnZXN1aXRlLm5ldC9XZWJPYmplY3RzL01aU3RvcmUud29hL3dhL2Jyb3dzZUFsYnVtPC9zdHJpbmc+CiAgICA8a2V5PnZpZXdBbGJ1bTwva2V5PjxzdHJpbmc+aHR0cDovL2F4LnBob2Jvcy5hcHBsZS5jb20uZWRnZXN1aXRlLm5ldC9XZWJPYmplY3RzL01aU3RvcmUud29hL3dhL3ZpZXdBbGJ1bTwvc3RyaW5nPgogICAgPGtleT52aWV3QXJ0aXN0PC9rZXk+PHN0cmluZz5odHRwOi8vYXgucGhvYm9zLmFwcGxlLmNvbS5lZGdlc3VpdGUubmV0L1dlYk9iamVjdHMvTVpTdG9yZS53b2Evd2Evdmlld0FydGlzdDwvc3RyaW5nPgo
gICAgPGtleT52aWV3Q29tcG9zZXI8L2tleT48c3RyaW5nPmh0dHA6Ly9heC5waG9ib3MuYXBwbGUuY29tLmVkZ2VzdWl0ZS5uZXQvV2ViT2JqZWN0cy9NWlN0b3JlLndvYS93YS92aWV3Q29tcG9zZXI8L3N0cmluZz4KICAgIDxrZXk+dmlld0dlbnJlPC9rZXk+PHN0cmluZz5odHRwOi8vYXgucGhvYm9zLmFwcGxlLmNvbS5lZGdlc3VpdGUubmV0L1dlYk9iamVjdHMvTVpTdG9yZS53b2Evd2Evdmlld0dlbnJlPC9zdHJpbmc+CiAgICA8a2V5PnZpZXdQb2RjYXN0PC9rZXk+PHN0cmluZz5odHRwOi8vYXgucGhvYm9zLmFwcGxlLmNvbS5lZGdlc3VpdGUubmV0L1dlYk9iamVjdHMvTVpTdG9yZS53b2Evd2Evdmlld1BvZGNhc3Q8L3N0cmluZz4KICAgIDxrZXk+dmlld1B1Ymxpc2hlZFBsYXlsaXN0PC9rZXk+PHN0cmluZz5odHRwOi8vYXgucGhvYm9zLmFwcGxlLmNvbS5lZGdlc3VpdGUubmV0L1dlYk9iamVjdHMvTVpTdG9yZS53b2Evd2Evdmlld1B1Ymxpc2hlZFBsYXlsaXN0PC9zdHJpbmc+CiAgICA8a2V5PnZpZXdWaWRlbzwva2V5PjxzdHJpbmc+aHR0cDovL2F4LnBob2Jvcy5hcHBsZS5jb20uZWRnZXN1aXRlLm5ldC9XZWJPYmplY3RzL01aU3RvcmUud29hL3dhL3ZpZXdWaWRlbzwvc3RyaW5nPgogICAgPGtleT5wb2RjYXN0czwva2V5PjxzdHJpbmc+aHR0cDovL2F4LnBob2Jvcy5hcHBsZS5jb20uZWRnZXN1aXRlLm5ldC9XZWJPYmplY3RzL01aU3RvcmUud29hL3dhL3ZpZXdQb2RjYXN0RGlyZWN0b3J5P
C9zdHJpbmc+CiAgICA8a2V5PmV4dGVybmFsVVJMU2VhcmNoS2V5PC9rZXk+PHN0cmluZz5heC5waG9ib3MuYXBwbGUuY29tLmVkZ2VzdWl0ZS5uZXQ8L3N0cmluZz4KICAgIDxrZXk+ZXh0ZXJuYWxVUkxSZXBsYWNlS2V5PC9rZXk+PHN0cmluZz5waG9ib3MuYXBwbGUuY29tPC9zdHJpbmc+CiAgICA8a2V5PnNlbGVjdGVkSXRlbXNQYWdlPC9rZXk+PHN0cmluZz5odHRwOi8vYXgucGhvYm9zLmFwcGxlLmNvbS5lZGdlc3VpdGUubmV0L1dlYk9iamVjdHMvTVpTdG9yZS53b2Evd2Evc2VsZWN0ZWRJdGVtc1BhZ2U8L3N0cmluZz4KCiAgICAKCiAgICAKCiAgICA8a2V5Pm1pbmktc3RvcmU8L2tleT48c3RyaW5nPmh0dHA6Ly9heC5waG9ib3MuYXBwbGUuY29tLmVkZ2VzdWl0ZS5uZXQvV2ViT2JqZWN0cy9NWlN0b3JlLndvYS93YS9taW5pc3RvcmVWMjwvc3RyaW5nPgogICAgPGtleT5taW5pLXN0b3JlLWZpZWxkczwva2V5PjxzdHJpbmc+YSxraW5kLHA8L3N0cmluZz4KICAgIDxrZXk+bWluaS1zdG9yZS1tYXRjaDwva2V5PjxzdHJpbmc+aHR0cDovL2F4LnBob2Jvcy5hcHBsZS5jb20uZWRnZXN1aXRlLm5ldC9XZWJPYmplY3RzL01aU3RvcmVTZXJ2aWNlcy53b2Evd2EvbWluaXN0b3JlTWF0Y2hWMjwvc3RyaW5nPgogICAgPGtleT5taW5pLXN0b3JlLW1hdGNoLWZpZWxkczwva2V5PjxzdHJpbmc+YW4sZ24sa2luZCxwbjwvc3RyaW5nPgogICAgPGtleT5taW5pLXN0b3JlLXdlbGNvbWU8L2tleT48c3RyaW5nPmh
0dHA6Ly9heC5waG9ib3MuYXBwbGUuY29tLmVkZ2VzdWl0ZS5uZXQvV2ViT2JqZWN0cy9NWlN0b3JlLndvYS93YS9taW5pc3RvcmVXZWxjb21lP3dpdGhDbGllbnRPcHRJbj0xPC9zdHJpbmc+CgogICAgPGtleT5jb3Zlci1hcnQ8L2tleT48c3RyaW5nPmh0dHA6Ly9heC5waG9ib3MuYXBwbGUuY29tLmVkZ2VzdWl0ZS5uZXQvV2ViT2JqZWN0cy9NWlN0b3JlU2VydmljZXMud29hL3dhL2NvdmVyQXJ0TWF0Y2g8L3N0cmluZz4KICAgIDxrZXk+Y292ZXItYXJ0LWZpZWxkczwva2V5PjxzdHJpbmc+YSxwPC9zdHJpbmc+CiAgICA8a2V5PmNvdmVyLWFydC1jZC1maWVsZHM8L2tleT48c3RyaW5nPmNkZGI8L3N0cmluZz4KICAgIDxrZXk+Y292ZXItYXJ0LW1hdGNoPC9rZXk+PHN0cmluZz5odHRwOi8vYXgucGhvYm9zLmFwcGxlLmNvbS5lZGdlc3VpdGUubmV0L1dlYk9iamVjdHMvTVpTdG9yZVNlcnZpY2VzLndvYS93YS9jb3ZlckFydE1hdGNoPC9zdHJpbmc+CiAgICA8a2V5PmNvdmVyLWFydC1tYXRjaC1maWVsZHM8L2tleT48c3RyaW5nPmNkZGIsYW4scG48L3N0cmluZz4KICAgIDxrZXk+Y292ZXItYXJ0LXVzZXI8L2tleT48c3RyaW5nPmh0dHA6Ly9waG9ib3MuYXBwbGUuY29tL1dlYk9iamVjdHMvTVpQZXJzb25hbGl6ZXIud29hL3dhL2NvdmVyQXJ0VXNlcjwvc3RyaW5nPgoKICAgIDxrZXk+bWF0Y2hVUkxzPC9rZXk+PGFycmF5PjxzdHJpbmc+aHR0cDovL3Bob2Jvcy5hcHBsZS5jb20vV2ViT2JqZWN0cy88L
3N0cmluZz48L2FycmF5PgoKICAgIAogICAgPGtleT5saWJyYXJ5LWxpbms8L2tleT48c3RyaW5nPmh0dHA6Ly9heC5waG9ib3MuYXBwbGUuY29tLmVkZ2VzdWl0ZS5uZXQvV2ViT2JqZWN0cy9NWlN0b3JlU2VydmljZXMud29hL3dhL2xpYnJhcnlMaW5rPC9zdHJpbmc+CiAgICAKICAgIDxrZXk+bGlicmFyeS1saW5rLWZpZWxkcy1saXN0PC9rZXk+CiAgICA8YXJyYXk+CiAgICAgIDxzdHJpbmc+YW4sY24sZ24sa2luZCxuLHBuPC9zdHJpbmc+CiAgICA8L2FycmF5PgogICAgCiAgICA8a2V5PmxpYnJhcnlMaW5rPC9rZXk+PHN0cmluZz5odHRwOi8vYXgucGhvYm9zLmFwcGxlLmNvbS5lZGdlc3VpdGUubmV0L1dlYk9iamVjdHMvTVpTdG9yZVNlcnZpY2VzLndvYS93YS9saWJyYXJ5TGluazwvc3RyaW5nPgoKICAgIAogICAgPGtleT5hdmFpbGFibGUtcmluZ3RvbmVzPC9rZXk+PHN0cmluZz5odHRwOi8vcGhvYm9zLmFwcGxlLmNvbS9XZWJPYmplY3RzL01aUGVyc29uYWxpemVyLndvYS93YS9hdmFpbGFibGVSaW5ndG9uZXM8L3N0cmluZz4KCiAgICAKCgogICAgPGtleT5tYXhDb21wdXRlcnM8L2tleT48c3RyaW5nPjU8L3N0cmluZz4KICAgIDxrZXk+bWF4UHVibGlzaGVkUGxheWxpc3RJdGVtczwva2V5PjxpbnRlZ2VyPjEwMDwvaW50ZWdlcj4KICAgIAogICAgPGtleT50cnVzdGVkRG9tYWluczwva2V5PgogICAgPGFycmF5PgogICAgICA8c3RyaW5nPi5hcHBsZS5jb208L3N0cmluZz4KICAgICAgPHN0cml
uZz4uYXBwbGUuY29tLmVkZ2VzdWl0ZS5uZXQ8L3N0cmluZz4KICAgICAgPHN0cmluZz5zdXBwb3J0Lm1hYy5jb208L3N0cmluZz4KICAgICAgPHN0cmluZz4uaXR1bmVzLmNvbTwvc3RyaW5nPgogICAgICA8c3RyaW5nPml0dW5lcy5jb208L3N0cmluZz4KICAgIDwvYXJyYXk+CgogICAgPGtleT5wbHVzLWluZm88L2tleT48c3RyaW5nPmh0dHA6Ly9heC5waG9ib3MuYXBwbGUuY29tLmVkZ2VzdWl0ZS5uZXQvV2ViT2JqZWN0cy9NWlN0b3JlLndvYS93YS9pVHVuZXNQbHVzTGVhcm5Nb3JlUGFnZTwvc3RyaW5nPgoKICAgIDxrZXk+YXBwbGV0di15b3V0dWJlLWF1dGgtdXJsPC9rZXk+PHN0cmluZz5odHRwczovL3d3dy5nb29nbGUuY29tLzwvc3RyaW5nPgogICAgPGtleT5hcHBsZXR2LXlvdXR1YmUtdXJsPC9rZXk+PHN0cmluZz5odHRwOi8vZ2RhdGEueW91dHViZS5jb20vPC9zdHJpbmc+CiAgICA8a2V5Pml0dW5lcy1wcmVzZW50cy1kaXJlY3RvcnktdXJsPC9rZXk+PHN0cmluZz5odHRwOi8vYXgucGhvYm9zLmFwcGxlLmNvbS5lZGdlc3VpdGUubmV0L1dlYk9iamVjdHMvTVpTdG9yZVNlcnZpY2VzLndvYS93cy9SU1MvZGlyZWN0b3J5PC9zdHJpbmc+CiAgICA8a2V5Pkdob3N0cmlkZXI8L2tleT48c3RyaW5nPllFUzwvc3RyaW5nPgoKICAgIDxrZXk+cDItdG9wLXRlbjwva2V5PjxzdHJpbmc+aHR0cDovL2F4LnBob2Jvcy5hcHBsZS5jb20uZWRnZXN1aXRlLm5ldC9XZWJPYmplY3RzL01aU3RvcmUud29hL
3dhL3ZpZXdUb3BUZW5zTGlzdDwvc3RyaW5nPgogICAgPGtleT5wMi1zZXJ2aWNlLXRlcm1zLXVybDwva2V5PjxzdHJpbmc+aHR0cDovL3d3dy5hcHBsZS5jb20vbGVnYWwvaXR1bmVzL3VrL3NlcnZpY2UuaHRtbDwvc3RyaW5nPgoKICAgIDxrZXk+bm93LXBsYXlpbmctdXJsPC9rZXk+PHN0cmluZz5odHRwOi8vYXgucGhvYm9zLmFwcGxlLmNvbS5lZGdlc3VpdGUubmV0L1dlYk9iamVjdHMvTVpTdG9yZS53b2Evd2Evbm93UGxheWluZzwvc3RyaW5nPgogICAgPGtleT5ub3ctcGxheWluZy1uZXR3b3JrLWRldGVjdC11cmw8L2tleT48c3RyaW5nPmh0dHA6Ly9heC5waG9ib3MuYXBwbGUuY29tLmVkZ2VzdWl0ZS5uZXQvV2ViT2JqZWN0cy9NWlN0b3JlLndvYS93YS9ub3dQbGF5aW5nPC9zdHJpbmc+CiAgICA8a2V5PmFkYW1pZC1sb29rdXAtdXJsPC9rZXk+PHN0cmluZz5odHRwOi8vYXgucGhvYm9zLmFwcGxlLmNvbS5lZGdlc3VpdGUubmV0L1dlYk9iamVjdHMvTVpTdG9yZS53b2Evd2EvYWRhbUlkTG9va3VwPC9zdHJpbmc+CgogICAgCgogICAgCgogICAgICAgIDxrZXk+YXV0aGVudGljYXRlQWNjb3VudDwva2V5PjxzdHJpbmc+aHR0cHM6Ly9waG9ib3MuYXBwbGUuY29tL1dlYk9iamVjdHMvTVpGaW5hbmNlLndvYS93YS9hdXRoZW50aWNhdGU8L3N0cmluZz4KICAgIDxrZXk+aVBob25lQWN0aXZhdGlvbjwva2V5PjxzdHJpbmc+aHR0cHM6Ly9hbGJlcnQuYXBwbGUuY29tL1dlYk9iamVjdHMvQUxBY3RpdmF
0aW9uLndvYS93YS9pUGhvbmVSZWdpc3RyYXRpb248L3N0cmluZz4KICAgIDxrZXk+ZGV2aWNlLWFjdGl2YXRpb248L2tleT48c3RyaW5nPmh0dHBzOi8vYWxiZXJ0LmFwcGxlLmNvbS9XZWJPYmplY3RzL0FMQWN0aXZhdGlvbi53b2Evd2EvZGV2aWNlQWN0aXZhdGlvbjwvc3RyaW5nPgogICAgPGtleT5hdXRob3JpemVNYWNoaW5lPC9rZXk+PHN0cmluZz5odHRwczovL3Bob2Jvcy5hcHBsZS5jb20vV2ViT2JqZWN0cy9NWkZpbmFuY2Uud29hL3dhL2F1dGhvcml6ZU1hY2hpbmU8L3N0cmluZz4KICAgIDxrZXk+YnV5UHJvZHVjdDwva2V5PjxzdHJpbmc+aHR0cHM6Ly9waG9ib3MuYXBwbGUuY29tL1dlYk9iamVjdHMvTVpGaW5hbmNlLndvYS93YS9idXlQcm9kdWN0PC9zdHJpbmc+CiAgICA8a2V5PmJ1eUNhcnQ8L2tleT48c3RyaW5nPmh0dHBzOi8vcGhvYm9zLmFwcGxlLmNvbS9XZWJPYmplY3RzL01aRmluYW5jZS53b2Evd2EvYnV5Q2FydDwvc3RyaW5nPgogICAgPGtleT5kZWF1dGhvcml6ZU1hY2hpbmU8L2tleT48c3RyaW5nPmh0dHBzOi8vcGhvYm9zLmFwcGxlLmNvbS9XZWJPYmplY3RzL01aRmluYW5jZS53b2Evd2EvZGVhdXRob3JpemVNYWNoaW5lPC9zdHJpbmc+CiAgICA8a2V5Pm1hY2hpbmVBdXRob3JpemF0aW9uSW5mbzwva2V5PjxzdHJpbmc+aHR0cHM6Ly9waG9ib3MuYXBwbGUuY29tL1dlYk9iamVjdHMvTVpGYXN0RmluYW5jZS53b2Evd2EvbWFjaGluZUF1dGhvcml6YXRpb25JbmZvPC9zdHJpb
mc+CiAgICA8a2V5Pm1vZGlmeUFjY291bnQ8L2tleT48c3RyaW5nPmh0dHBzOi8vcGhvYm9zLmFwcGxlLmNvbS9XZWJPYmplY3RzL01aRmluYW5jZS53b2Evd2EvYWNjb3VudFN1bW1hcnk8L3N0cmluZz4KICAgIDxrZXk+cGVuZGluZ1NvbmdzPC9rZXk+PHN0cmluZz5odHRwczovL3Bob2Jvcy5hcHBsZS5jb20vV2ViT2JqZWN0cy9NWkZpbmFuY2Uud29hL3dhL3BlbmRpbmdTb25nczwvc3RyaW5nPgogICAgPGtleT5zaWdudXA8L2tleT48c3RyaW5nPmh0dHBzOi8vcGhvYm9zLmFwcGxlLmNvbS9XZWJPYmplY3RzL01aRmluYW5jZS53b2Evd2Evc2lnbnVwV2l6YXJkPC9zdHJpbmc+CiAgICA8a2V5PnNvbmdEb3dubG9hZERvbmU8L2tleT48c3RyaW5nPmh0dHBzOi8vcGhvYm9zLmFwcGxlLmNvbS9XZWJPYmplY3RzL01aRmFzdEZpbmFuY2Uud29hL3dhL3NvbmdEb3dubG9hZERvbmU8L3N0cmluZz4KICAgIDxrZXk+Zm9yZ290dGVuUGFzc3dvcmQ8L2tleT48c3RyaW5nPmh0dHBzOi8vcGhvYm9zLmFwcGxlLmNvbS9XZWJPYmplY3RzL01aRmluYW5jZS53b2Evd2EvaUZvcmdvdDwvc3RyaW5nPgogICAgPGtleT5teUluZm88L2tleT48c3RyaW5nPmh0dHBzOi8vbXlpbmZvLmFwcGxlLmNvbS88L3N0cmluZz4KICAgIDxrZXk+bm9BT0xBY2NvdW50czwva2V5PjxmYWxzZS8+CiAgICA8a2V5PnVwbG9hZFB1Ymxpc2hlZFBsYXlsaXN0PC9rZXk+PHN0cmluZz5odHRwczovL3Bob2Jvcy5hcHBsZS5jb20vV2ViT2JqZWN
0cy9NWkZpbmFuY2Uud29hL3dhL3VwbG9hZFB1Ymxpc2hlZFBsYXlMaXN0PC9zdHJpbmc+CiAgICA8a2V5PmxvZ291dDwva2V5PjxzdHJpbmc+aHR0cHM6Ly9waG9ib3MuYXBwbGUuY29tL1dlYk9iamVjdHMvTVpGaW5hbmNlLndvYS93YS9sb2dvdXQ8L3N0cmluZz4KICAgIDxrZXk+YWRkVG9DYXJ0PC9rZXk+PHN0cmluZz5odHRwczovL3Bob2Jvcy5hcHBsZS5jb20vV2ViT2JqZWN0cy9NWkZpbmFuY2Uud29hL3dhL2FkZFRvQ2FydDwvc3RyaW5nPgogICAgPGtleT5yZW1vdmVGcm9tQ2FydDwva2V5PjxzdHJpbmc+aHR0cHM6Ly9waG9ib3MuYXBwbGUuY29tL1dlYk9iamVjdHMvTVpGaW5hbmNlLndvYS93YS9yZW1vdmVGcm9tQ2FydDwvc3RyaW5nPgogICAgPGtleT5zaG9wcGluZ0NhcnQ8L2tleT48c3RyaW5nPmh0dHBzOi8vcGhvYm9zLmFwcGxlLmNvbS9XZWJPYmplY3RzL01aRmluYW5jZS53b2Evd2Evc2hvcHBpbmdDYXJ0PC9zdHJpbmc+CiAgICA8a2V5PmJjVVJMczwva2V5PjxhcnJheT48c3RyaW5nPmh0dHA6Ly8ucGhvYm9zLmFwcGxlLmNvbTwvc3RyaW5nPjxzdHJpbmc+aHR0cDovL3d3dy5hdGRtdC5jb208L3N0cmluZz48L2FycmF5PgogICAgPGtleT51cGdyYWRlUGhvbmU8L2tleT48c3RyaW5nPmh0dHBzOi8vcGhvYm9zLmFwcGxlLmNvbS9XZWJPYmplY3RzL01aRmluYW5jZS53b2Evd2EvdXBncmFkZVBob25lPC9zdHJpbmc+CiAgICA8a2V5PnVwZ3JhZGVEcm08L2tleT48c3RyaW5nPmh0dHBzO
i8vcGhvYm9zLmFwcGxlLmNvbS9XZWJPYmplY3RzL01aRmluYW5jZS53b2Evd2EvdXBncmFkZURybTwvc3RyaW5nPgogICAgPGtleT5yZXBvcnRQb2RjYXN0PC9rZXk+PHN0cmluZz5odHRwczovL3Bob2Jvcy5hcHBsZS5jb20vV2ViT2JqZWN0cy9NWkZpbmFuY2Uud29hL3dhL3JlcG9ydFBvZGNhc3Q8L3N0cmluZz4KICAgIDxrZXk+Z2lmdFBsYXlsaXN0PC9rZXk+PHN0cmluZz5odHRwczovL3Bob2Jvcy5hcHBsZS5jb20vV2ViT2JqZWN0cy9NWkZpbmFuY2Uud29hL3dhL2dpZnRTb25nc1dpemFyZDwvc3RyaW5nPgogICAgPGtleT5naXZlLXBsYXlsaXN0PC9rZXk+PHN0cmluZz5odHRwczovL3Bob2Jvcy5hcHBsZS5jb20vV2ViT2JqZWN0cy9NWkZpbmFuY2Uud29hL3dhL2dpZnRTb25nc1dpemFyZDwvc3RyaW5nPgogICAgPGtleT5jaGVjay1kb3dubG9hZC1xdWV1ZTwva2V5PjxzdHJpbmc+aHR0cHM6Ly9waG9ib3MuYXBwbGUuY29tL1dlYk9iamVjdHMvTVpGaW5hbmNlLndvYS93YS9jaGVja0Rvd25sb2FkUXVldWU8L3N0cmluZz4KICAgIDxrZXk+c2V0LWF1dG8tZG93bmxvYWQ8L2tleT48c3RyaW5nPmh0dHBzOi8vcGhvYm9zLmFwcGxlLmNvbS9XZWJPYmplY3RzL01aRmluYW5jZS53b2Evd2Evc2V0QXV0b0Rvd25sb2FkPC9zdHJpbmc+CiAgICA8a2V5Pm5ldy1pcG9kLXVzZXI8L2tleT48c3RyaW5nPmh0dHBzOi8vcGhvYm9zLmFwcGxlLmNvbS9XZWJPYmplY3RzL01aRmluYW5jZS53b2Evd2EvaVBvZFJ
lZ2lzdHJhdGlvbjwvc3RyaW5nPgogICAgPGtleT5uZXctdHYtdXNlcjwva2V5PjxzdHJpbmc+aHR0cHM6Ly9waG9ib3MuYXBwbGUuY29tL1dlYk9iamVjdHMvTVpGaW5hbmNlLndvYS93YS9pVFZSZWdpc3RyYXRpb248L3N0cmluZz4KICAgIDxrZXk+bWQ1LW1pc21hdGNoPC9rZXk+PHN0cmluZz5odHRwczovL3Bob2Jvcy5hcHBsZS5jb20vV2ViT2JqZWN0cy9NWkZpbmFuY2Uud29hL3dhL21kNU1pc21hdGNoPC9zdHJpbmc+CiAgICA8a2V5PnJlcG9ydC1lcnJvcjwva2V5PjxzdHJpbmc+aHR0cHM6Ly9waG9ib3MuYXBwbGUuY29tL1dlYk9iamVjdHMvTVpGaW5hbmNlLndvYS93YS9yZXBvcnRFcnJvckZyb21DbGllbnQ8L3N0cmluZz4KICAgIDxrZXk+dXBkYXRlQXNzZXQ8L2tleT48c3RyaW5nPmh0dHBzOi8vcGhvYm9zLmFwcGxlLmNvbS9XZWJPYmplY3RzL01aRmluYW5jZS53b2Evd2EvdXBkYXRlQXNzZXQ8L3N0cmluZz4KICAgIDxrZXk+Y3JlYXRlLXRva2VuPC9rZXk+PHN0cmluZz5odHRwczovL3Bob2Jvcy5hcHBsZS5jb20vV2ViT2JqZWN0cy9NWkZpbmFuY2Uud29hL3dhL2NyZWF0ZVRva2VuPC9zdHJpbmc+CiAgICA8a2V5PmNyZWF0ZS1zZXNzaW9uPC9rZXk+PHN0cmluZz5odHRwczovL3Bob2Jvcy5hcHBsZS5jb20vV2ViT2JqZWN0cy9NWkZpbmFuY2Uud29hL3dhL2NyZWF0ZVNlc3Npb248L3N0cmluZz4KICAgIAoKICAgICAgCiAgICAgIAogICAgPC9kaWN0PgogIDwvcGxpc3Q+CgoK</data>
		</dict>
	</plist>'''

	COVER_INFO_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<Document xmlns="http://www.apple.com/itms/" disableHistory="true" disableNavigation="true">
	<Protocol>
		<plist version="1.0">
			<dict>
				<key>status</key><integer>0</integer>
				<key>cover-art-url</key><string>http://localhost/serve?key=%s</string>
				<key>request-delay-seconds</key><string>.1</string>
				<key>artistName</key><string></string>
				<key>playlistName</key><string></string>
				<key>artistId</key><string></string>
				<key>playlistId</key><string></string>
				<key>matchType</key><string>2</string>
			</dict>
		</plist>
	</Protocol>
</Document>'''

	NO_COVER_FOUND_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<Document xmlns="http://www.apple.com/itms/" disableHistory="true" disableNavigation="true">
	<Protocol>
		<plist version="1.0">
			<dict>
				<key>status</key><integer>3004</integer>
				<key>cover-art-url</key><string></string>
				<key>request-delay-seconds</key><string>.1</string>
			</dict>
		</plist>
	</Protocol>
</Document>'''

	def do_GET(self):
		urlParts = urlparse.urlparse(self.path)
		location = urlParts[2]
		query = cgi.parse_qs(urlParts[4])
		self.handleRequest(location, query)

	def do_POST(self):
		urlParts = urlparse.urlparse(self.path)
		location = urlParts[2]
		cl = int(self.headers['Content-Length'])
		data = self.rfile.read(cl)
		query = cgi.parse_qs(data)
		self.handleRequest(location, query)

	def handleRequest(self, location, query):
		# Display the frame set for our web site.
		if location == '/':
			self.sendTemplate("frameset.tmpl")

		# Display the album list for the left frame of our web site.
		elif location == '/list':
			tags = {"albums": albumDB.getAllRecords(), "urllib":urllib}
			self.sendTemplate("list.tmpl", tags)

		# Display the album details for the right frame of our web site,
		# or save changes to the selected album.
		elif location == '/view' or location == '/save':
			tags = {"response":"", "selection":None, "covers":None, "key":None, "urllib":urllib}
			if "key" not in query:
				self.sendTemplate("album.tmpl", tags)
				return
			tags["key"] = query['key'][0]
			tags["selection"] = albumDB.get(tags["key"])
			if not tags["selection"]:
				tags["response"] = "Album not found"
			elif "searchTerms" not in query:
				aca = amazonCoverArt.AmazonCoverArt()
				tags["covers"] = aca.search(artist=tags["selection"]["artist"], album=tags["selection"]["album"])
				if len(tags["covers"]) == 0:
					tags["response"] = "No covers found"

			if location == '/save':
				if "clear" in query:
					albumDB.setField(tags["key"], "url", "")
					tags["response"] = 'The cover art was cleared'
				elif "searchTerms" in query:
					aca = amazonCoverArt.AmazonCoverArt()
					tags["covers"] = aca.search(keywords=query["searchTerms"][0])
					if len(tags["covers"]) == 0:
						tags["response"] = "No covers found"
				elif "url" in query:
					albumDB.setField(tags["key"], "url", query["url"][0])
					albumDB.save()
					tags["response"] = 'Your selection was saved'
				else: tags["response"] = 'Unable to save'

			self.sendTemplate("album.tmpl", tags)

		# Send an individual album cover image to iTunes.
		elif location == '/serve':
			key = query['key'][0]
			record = albumDB.get(key)
			if record and "url" in record:
				self.sendCover(record["url"])
			else: self.sendXML(self.NO_COVER_FOUND_XML)

		# Called when iTunes asks for artwork for the first time
		elif location == '/WebObjects/MZStore.woa/wa/initiateSession':
			self.sendXML(self.INIT_SESSION_XML)

		# This is called when we choose "Get Album Artwork" in iTunes.
		# If we haven't selected a cover for this album, add it to our database.
		# If we have, send a fake XML response to iTunes, to tell it where to get the cover.
		# This response actually points back to our /serve URL.
		elif location == '/WebObjects/MZSearch.woa/wa/coverArtMatch' or location == '/WebObjects/MZStoreServices.woa/wa/coverArtMatch':
			key = md5.new(query['an'][0] + '/' + query['pn'][0]).hexdigest()
			record = albumDB.get(key)
			if record:
				if "url" in record:
					self.sendXML(self.COVER_INFO_XML % urllib.quote_plus(key))
				else: self.sendXML(self.NO_COVER_FOUND_XML)
			else:
				albumDB.add(key, {"artist":query['an'][0], "album":query['pn'][0]})
				self.sendXML(self.NO_COVER_FOUND_XML)

		else: self.send_error(404)

	def sendXML(self, xmlStr):
		self.send_response(200)
		self.send_header('Content-type', 'text/xml; charset=UTF-8')
		self.end_headers()
		self.wfile.write(xmlStr.encode('utf-8'))

	def sendTemplate(self, tmplFile, tags = {}):
		f = open(tmplFile, 'r')
		text = f.read()
		f.close()
		tmpl = stpy.Template(text)
		self.send_response(200)
		self.send_header('Content-type', 'text/html; charset=UTF-8')
		self.end_headers()
		print >> self.wfile, tmpl.render(tags)

	def sendCover(self, url):
		try:
			f = None
			f = urllib.urlopen(url)
			type = f.info().gettype()
			if type in self.VALID_TYPES:
				imgData = f.read()
				f.close()
				self.send_response(200)
				self.send_header('Content-type', type)
				self.end_headers()
				self.wfile.write(imgData)
				return
		except:
			print "Can't read image"
			if f: f.close()
		self.sendXML(self.NO_COVER_FOUND_XML)

def main():
	global albumDB
	albumDB = albumDatabase.AlbumDatabase()
	try:
		server = BaseHTTPServer.HTTPServer(('', CoverArtServer.SERVER_PORT), CoverArtServer)
		server.serve_forever()
	except KeyboardInterrupt:
		server.socket.close()
	except:
		print "Could not start server"
	albumDB.save()

if __name__ == '__main__':
    main()
