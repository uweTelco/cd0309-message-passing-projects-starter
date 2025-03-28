import grpc
from person_pb2 import empty
from person_pb2_grpc import PersonServiceStub

if __name__ == "__main__":
    print('Hello World')
    channel = grpc.insecure_channel('localhost:30011')  # Ensure this matches your server address
    stub = PersonServiceStub(channel)
    # Prepare the empty request
    empty_request = empty()

    # Call the RPC
    #response = stub.Get(empty_request)
    try:
        response = stub.Get(empty_request)
    except grpc.RpcError as e:
        print( e)
        
    print(response)
