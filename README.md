## Description
Develop and fix endpoints for handling activity logs. This includes creating new activity logs, retrieving all activity logs, and retrieving activity logs for a specific user.

## Purpose
Implement endpoints to facilitate the creation and retrieval of activity logs for users.

## Requirements
- Implement a POST endpoint to create new activity logs.
- Implement a GET endpoint to retrieve all activity logs.
- Implement a GET endpoint to retrieve activity logs for a specific user by user ID.
  
## Acceptance Criteria
## POST /activity-log
- Purpose: Create a new activity log.
- Requirements:
  - Validate the request body.
  - Save the new activity log to the database.
- Status Codes:
  - 201 Created: For successful creation.
  - 400 Bad Request: For validation errors.
  - 401 Unauthorized: For authentication issues.
## GET /activity-log
- Purpose: Retrieve all activity logs.
- Requirements:
  - Fetch all activity logs from the database.
- Status Codes:
  - 200 OK: For successful retrieval.
  - 401 Unauthorized: For authentication issues.
## GET /activity-log/{user-id}
- Purpose: Retrieve activity logs for a specific user.
- Requirements:
  - Fetch activity logs for the specified user from the database.
Status Codes:
  - 200 OK: For successful retrieval.
  - 404 Not Found: If no activity logs are found for the user.
  - 401 Unauthorized: For authentication issues.
## Response Formats
## Successful Creation Response
  - Status Code: 201 Created
  - Message: Activity log created successfully.
  - Example:
```
{
  "status": "success",
  "message": "Activity log created successfully.",
  "status_code": 201
}
```
## Successful Retrieval Response
 - Status Code: 200 OK
 - Message: Activity logs retrieved successfully.
 - Example:
```
{
  "status": "success",
  "message": "Activity logs retrieved successfully.",
  "status_code": 200,
  "data": []
}
```

## Invalid Input or Unauthorized Response
  - Status Code: 400 Bad Request
  - Message: Invalid input or authentication issues.
  - Example:
```
{
  "status": "error",
  "message": "Invalid input or authentication issues.",
  "status_code": 400
}

```

## User Not Found Response

 - Status Code: 404 Not Found
 - Message: User not found.
 - Example:
```
{
  "status": "error",
  "message": "User not found.",
  "status_code": 404
}
```

## Checklist

## Input Validation
  - Validate that all required fields are present in the request body for POST requests.
  - Ensure the data meets the required format and criteria.
## User Lookup
  - Ensure the user exists in the database using the provided user ID for GET requests.
## Authentication
  - Verify that the user is authenticated for all requests.
  - Ensure the request includes a valid token.
## Data Processing
  - Fetch the relevant data from the database.
  - Save the new activity logs to the database for POST requests.
## Security Best Practices
  - Implement HTTPS to secure data in transit.
  - Implement rate limiting to prevent brute force attacks.
  - Log and monitor activity log requests for suspicious activity.
## Notifications and Logs
  - Maintain audit logs of activity log requests for forensic purposes.
## Unit Tests
## POST /activity-log Endpoint
  - Test that the endpoint processes the activity log creation request correctly.
  - Mock the data access layer to simulate different scenarios.
  - Verify that the response includes appropriate status codes and messages for various outcomes (successful creation, invalid input, authentication issues).
## GET /activity-log Endpoint
  - Test that the endpoint retrieves all activity logs correctly.
  - Mock the data access layer to simulate different scenarios.
  - Verify that the response includes appropriate status codes and messages for successful retrieval and authentication issues.
## GET /activity-log/{user-id} Endpoint
  - Test that the endpoint retrieves activity logs for a specific user correctly.
  - Mock the data access layer to simulate different scenarios.
  - Verify that the response includes appropriate status codes and messages for various ou
