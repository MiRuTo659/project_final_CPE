from onvif import ONVIFCamera

cam = ONVIFCamera('192.168.137.61', 80, 'admin', '1234')
media_service = cam.create_media_service()
profiles = media_service.GetProfiles()
stream_uri = media_service.GetStreamUri({
    'StreamSetup': {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}},
    'ProfileToken': profiles[0].token
})
print(f"RTSP URL: {stream_uri.Uri}")
