import turtle
import time
from winsdk._winrt import initialize_with_window
from winsdk.windows.foundation import IAsyncOperation, AsyncStatus
from winsdk.windows.graphics.capture import Direct3D11CaptureFramePool,GraphicsCapturePicker, GraphicsCaptureItem

def on_pick_completed(op: IAsyncOperation, status: AsyncStatus) -> None:
    if status == AsyncStatus.ERROR:
        print("error: ", status.error_code.value)
    elif status == AsyncStatus.CANCELED:
        # this is programatically, canceled, not user canceled
        print("operation canceled")
    elif status == AsyncStatus.COMPLETED:
        result: Optional[GraphicsCaptureItem] = op.get_results()
        if result:
            print("result:",  result.display_name)
        else:
            print("user canceled")

    op.close()

picker = GraphicsCapturePicker()
# initialize_with_window(picker, turtle.getcanvas().winfo_id())
op = picker.pick_single_item_async()
op.completed = on_pick_completed

time.sleep(10)
