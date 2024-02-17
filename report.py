import json

def generate_html_report(json_file, output_file):
    # Read JSON data from file
    with open(json_file) as f:
        data = json.load(f)
    
    # Extract the list of workspaces
    workspaces = data.get('Workspaces', [])
    
    # Extract unique compute type names
    compute_types = set()
    for workspace in workspaces:
        compute_types.add(workspace.get('WorkspaceProperties', {}).get('ComputeTypeName', 'N/A'))
    
    # Start building HTML content
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<title>Workspaces Report</title>
<style>
    body {{
        font-family: Arial, sans-serif;
    }}
    h1 {{
        color: #333;
        text-align: center;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
    }}
    th, td {{
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }}
    th {{
        background-color: #f2f2f2;
    }}
    .null {{
        color: #FF0000;
    }}
    .filter {{
        margin-bottom: 10px;
    }}
</style>
</head>
<body>
<h1>Workspaces Report </h1>
<div class="filter">
    <label for="compute-type">Filter by Compute Type:</label>
    <select id="compute-type" onchange="filterByComputeType(this.value)">
        <option value="">All</option>
"""

    # Add options for compute type filter
    for compute_type in compute_types:
        html_content += f"<option value='{compute_type}'>{compute_type}</option>\n"
    
    html_content += """
    </select>
</div>
<p id="total-workspaces">Total number of workspaces: </p>
<p id="total-null">Total number without activity: </p>
<p id="total-date">Total number with date record: </p>
<table id="workspaces-table">
<tr><th>Directory ID</th><th>User Name</th><th>Workspace ID</th><th>IP Address</th><th>Last Known User Connection</th><th>Compute Type Name</th><th>Bundle ID</th></tr>
"""

    # Add rows for each workspace
    for workspace in workspaces:
        # Check if the workspace is a dictionary
        if isinstance(workspace, dict):
            html_content += "<tr>\n"
            html_content += f"<td>{workspace.get('DirectoryId', 'N/A')}</td>\n"
            html_content += f"<td>{workspace.get('UserName', 'N/A')}</td>\n"
            html_content += f"<td>{workspace.get('WorkspaceId', 'N/A')}</td>\n"
            html_content += f"<td>{workspace.get('IpAddress', 'N/A')}</td>\n"
            last_known_timestamp = workspace.get('LastKnownUserConnectionTimestamp')
            if last_known_timestamp is not None:
                html_content += f"<td>{last_known_timestamp}</td>\n"
            else:
                html_content += "<td class='null'>NULL</td>\n"
            html_content += f"<td>{workspace.get('WorkspaceProperties', {}).get('ComputeTypeName', 'N/A')}</td>\n"
            html_content += f"<td>{workspace.get('BundleId', 'N/A')}</td>\n"
        else:
            print(f"Invalid workspace format: {workspace}")

    html_content += "</table>\n"
    html_content += "<script>\n"
    html_content += """
function filterByComputeType(computeType) {
    var rows = document.querySelectorAll('#workspaces-table tr');
    var totalWorkspaces = 0;
    var totalNull = 0;
    var totalDate = 0;
    for (var i = 1; i < rows.length; i++) {
        var row = rows[i];
        var computeTypeCell = row.cells[5]; // index of Compute Type Name column
        var nullCell = row.cells[4]; // index of Last Known User Connection Timestamp column
        if (computeType === '' || computeTypeCell.textContent === computeType) {
            row.style.display = '';
            totalWorkspaces++;
            if (nullCell.textContent === 'NULL') {
                totalNull++;
            } else {
                totalDate++;
            }
        } else {
            row.style.display = 'none';
        }
    }
    document.getElementById('total-workspaces').textContent = 'Total number of workspaces: ' + totalWorkspaces;
    document.getElementById('total-null').textContent = 'Total number without activity: ' + totalNull;
    document.getElementById('total-date').textContent = 'Total number with date record: ' + totalDate;
}
"""
    html_content += "</script>\n"
    html_content += "</body>\n</html>"
    
    # Write HTML content to output file
    with open(output_file, 'w') as f:
        f.write(html_content)

if __name__ == '__main__':
    json_file = 'workspaces.json'
    output_file = 'workspaces_report.html'
    generate_html_report(json_file, output_file)
