import win32api
import win32con
import win32security


def is_process_admin(pid):
    try:
        # Open a handle to the process
        hProcess = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid)
        # Open the process token
        hToken = win32security.OpenProcessToken(hProcess, win32con.TOKEN_QUERY)

        # Get the SID for the Administrators group
        adminSid = win32security.CreateWellKnownSid(win32security.WinBuiltinAdministratorsSid, None)

        # Check if the token has the admin SID
        isAdmin = win32security.CheckTokenMembership(hToken, adminSid)

        return isAdmin
    except Exception as e:
        print(f"Error checking process privileges: {e}")
        return False


# Example usage
pid = 27988  # Replace with your target PID
if is_process_admin(pid):
    print("The process is running with administrative privileges.")
else:
    print("The process is not running with administrative privileges.")
