import asyncio

from winsdk.windows.media.capture import MediaCapture

media_capture = MediaCapture()


# asyncio.run(media_capture.initialize_async())
#
async def init_mediacapture():
    await media_capture.initialize_async()


# media_capture.initialize_async()
asyncio.run(init_mediacapture())
# direct_3d_device = media_capture.media_capture_settings and media_capture.media_capture_settings.direct3_d11_device
# if not direct_3d_device:
#     try:
#         # May be problematic? https://github.com/pywinrt/python-winsdk/issues/11#issuecomment-1315345318
#         direct_3d_device = LearningModelDevice(LearningModelDeviceKind.DIRECT_X_HIGH_PERFORMANCE).direct3_d11_device
#     # TODO: Unknown potential error, I don't have an older Win10 machine to test.
#     except BaseException:  # noqa: S110,BLE001
#         pass
# if not direct_3d_device:
#     raise OSError("Unable to initialize a Direct3D Device.")
