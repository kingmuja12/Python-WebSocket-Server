########################################################
# WebSocket with Python (Server)
########################################################
import socket 
import websockets 
import asyncio
import traceback

# Get the hostname of the server machine
Host_name = socket.gethostname()
print(Host_name)

# Retrieve the private IP address of the server
# The server connects to a public DNS server (Google's 8.8.8.8) temporarily to determine its private IP.
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as P:
    P.connect(('8.8.8.8', 53))  # Connect to the DNS server
    IP_address = P.getsockname()  # Get the socket's IP address and port
    My_IP = IP_address[0]  # Extract the IP address
    print(My_IP)  # Print the private IP

#############################
# Port Scanner for Clients
#############################

async def port_scan():
    """
    This function scans the local network for devices attempting to connect.
    It ensures only devices within the local private network can connect.
    """
    # Check if the IP is within the local network range.
    # Replace '<the first 3 digit of your IP>', '<the second 3 digit>', etc., with actual values.
    if not My_IP[:3] == '<the first 3 digit of your IP>' and not My_IP[4:7] == '<the second 3 digit of your IP>' and not My_IP[8:9] == '<the single digit after>': 
        print("This device you are using is not connected to the private network!!!")
        print("Unauthorized access detected! Exiting.")
        exit()

    # Define the base range of the private network (first three octets of IP)
    IP_range = My_IP[:9]

    # Scan through IPs in the range 1-254 (common for LANs)
    i = 0
    while i < 255:
        i += 1
        target_ip = f"{IP_range}.{i}"  # Construct the target IP
        print(target_ip)  # Print the current IP being scanned

        url = f"ws://{target_ip}:5859"  # Construct WebSocket URL
        try:
            # Attempt to connect to the target IP using WebSocket
            connect_clients = await asyncio.wait_for(websockets.connect(url), timeout=5)
            await connect_clients.send("Hello from the server!")  # Send a message upon successful connection
            print("Connection successful")
        except ConnectionRefusedError:
            print("Client refused connection")
            pass  # Skip to the next IP if the connection is refused
        except ConnectionError:
            pass  # Handle generic connection errors
        except TimeoutError:
            print("Connection timed out")
            pass  # Skip if the target does not respond in time
        except:  
            # Handle unexpected errors during the connection process
            traceback.print_exc()

################################################################
# WebSocket Handler
################################################################

async def websocket_handler(websocket, _):
    """
    Handles incoming WebSocket connections and messages.
    """
    async for message in websocket:
        print(message)  # Print any message received from a client

################################################################
# Main Execution
################################################################

if __name__ == '__main__':
    # Start the WebSocket server on the server's private IP and port 5859
    start_server = websockets.serve(websocket_handler, My_IP, 5859)
    
    # Run the server and port scanner concurrently
    asyncio.get_event_loop().run_until_complete(start_server)  # Start the WebSocket server
    asyncio.get_event_loop().run_until_complete(port_scan())  # Run the port scanner
    
    # Keep the server running indefinitely
    asyncio.get_event_loop().run_forever()

