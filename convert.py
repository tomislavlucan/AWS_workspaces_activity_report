import json
import boto3
from datetime import datetime

def get_workspaces_from_file(json_file):
    with open(json_file) as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    return data.get('Workspaces', [])

def count_timestamps(workspaces):
    timestamp_count = 0
    null_count = 0
    for workspace in workspaces:
        if workspace.get('LastKnownUserConnectionTimestamp'):
            timestamp_count += 1
        else:
            null_count += 1
    return timestamp_count, null_count

def get_last_known_user_connection_timestamp(client, workspace_id):
    retries = 5
    delay = 1
    for _ in range(retries):
        try:
            response = client.describe_workspaces_connection_status(WorkspaceIds=[workspace_id])
            connection_status_list = response.get('WorkspacesConnectionStatus', [])
            if connection_status_list:
                connection_status = connection_status_list[0]
                last_known_user_connection_timestamp = connection_status.get('LastKnownUserConnectionTimestamp')
                if last_known_user_connection_timestamp:
                    last_known_user_connection_timestamp = last_known_user_connection_timestamp.strftime('%Y-%m-%d %H:%M:%S')
                return last_known_user_connection_timestamp
            else:
                return None  # or any appropriate value
        except client.exceptions.ThrottlingException as e:
            print(f"Throttling exception encountered. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2
    raise Exception("Max retries exceeded. Unable to retrieve connection status.")


def update_json_file(json_file, client, workspaces):
    total_workspaces = len(workspaces)
    print("Updating workspaces:")
    for idx, workspace in enumerate(workspaces, start=1):
        workspace_id = workspace['WorkspaceId']
        last_known_user_connection_timestamp = get_last_known_user_connection_timestamp(client, workspace_id)
        workspace['LastKnownUserConnectionTimestamp'] = last_known_user_connection_timestamp

        # Print progress
        print(f"Processed {idx}/{total_workspaces} workspaces...", end='\r')
    
    with open(json_file, 'w') as f:
        json.dump({'Workspaces': workspaces}, f, indent=4, default=str)

    print("\nUpdate complete.")

if __name__ == '__main__':
    json_file = 'workspaces.json'
    client = boto3.client('workspaces')
    workspaces = get_workspaces_from_file(json_file)
    update_json_file(json_file, client, workspaces)
    timestamp_count, null_count = count_timestamps(workspaces)

    print("Report:")
    print(f"Total workspaces with LastKnownUserConnectionTimestamp: {timestamp_count}")
    print(f"Total workspaces with NULL LastKnownUserConnectionTimestamp: {null_count}")
