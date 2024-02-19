#!/usr/bin/env python3
"""
Image Downloader with MITMProxy.

This script captures and downloads images from HTTP responses.

Usage:
  mitmdump -s image_downloader.py

Example:
  mitmdump -s image_downloader.py
"""

from mitmproxy import http

def response(packet):
    """
    Processes HTTP responses and downloads images.

    Args:
        packet (mitmproxy.http.HTTPFlow): The HTTP packet to process.
    """
    content_type = packet.response.headers.get("content-type", "")

    try:
        if "image" in content_type:
            url = packet.request.url
            extension = content_type.split("/")[-1]

            if extension == "jpeg":
                extension = "jpg"

            file_name = f"images/{url.replace('/', '_').replace(':', '_')}.{extension}"
            image_data = packet.response.content

            with open(file_name, "wb") as f:
                f.write(image_data)

            print(f"[+] Image saved: {file_name}")

    except:
        pass
