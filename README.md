# Ride Management
Ride Management is an API endpoints created using Django-based Rest API application to manage ride events, rides and users. This api endpoints are able to handle riders, drivers, and to track status of rides and events.

# Features
- `User Authentication`: Token-based authentication (JWT) to secure the API.
- `CRUD Operations`: Allows creation, reading, updating, and deletion of rides, ride events, and users.
- `Pagination & Filtering`: Supports pagination and filtering of rides based on pickup time, status, and rider email.
- `Sorting`: Ability to sort rides based on pickup time and distance from a given GPS position.
- `Admin Access`: Only users with the 'admin' role are authorized to access certain endpoints.
- `Performance Optimized`: Efficient queries to handle large datasets, especially for ride events.

# Installation
### 1. Clone the repository
    ```sh
    git clone https://github.com/JARevilla/RideManagement.git
    cd RideManagement
    ```

### 2. Create and activate a virtual environment
    ```sh
    python -m venv venv
    source venv/bin/activate    # If using Windows OS then use venv\Scripts\activate to activate virtual environment
    ```

### 3. Install dependencies
    ```sh
    pip install -r requirements.txt
    ```

### 4. Apply migrations
    ```sh
    python manage.py migrate
    ```

### 5. Create a superuser
    ```sh
    python manage.py createsuperuser
    ```

### 6. Run server
    ```sh
    python manage.py runserver
    ```


# API Endpoints
- `POST /api/api-token-auth/` - Obtain authentication token.
- `GET /api/rides/` - List all rides with pagination and filtering options.
- `POST /api/rides/` - Create a new ride.
- `GET /api/rides/{id}/` - Retrieve a specific ride.
- `PUT /api/rides/{id}/` - Update an existing ride.
- `DELETE /api/rides/{id}/` - Delete a ride.
- `GET /api/ride-events/` - List all ride events.
- `POST /api/ride-events/ `- Create a new ride event.
- `GET /api/ride-events/{id}/` - Retrieve a specific ride event.
- `PUT /api/ride-events/{id}/` - Update an existing ride event.
- `DELETE /api/ride-events/{id}/` - Delete a ride event..


# SQL Query for Reporting

```sql
WITH RideDurations AS (
    SELECT
        r.id_ride,
        r.id_driver,
        EXTRACT(YEAR FROM r.pickup_time) AS year,
        EXTRACT(MONTH FROM r.pickup_time) AS month,
        -- Get the pickup and dropoff times for each ride
        MAX(CASE WHEN re.description = 'Status changed to pickup' THEN re.created_at END) AS pickup_time,
        MAX(CASE WHEN re.description = 'Status changed to dropoff' THEN re.created_at END) AS dropoff_time
    FROM
        rides_ride r
    LEFT JOIN
        rides_rideevent re ON r.id_ride = re.id_ride
    WHERE
        re.description IN ('Status changed to pickup', 'Status changed to dropoff')
    GROUP BY
        r.id_ride, r.id_driver, r.pickup_time
)
SELECT
    TO_CHAR(DATE_TRUNC('month', TO_TIMESTAMP(year || '-' || month || '-01', 'YYYY-MM-DD')), 'YYYY-MM') AS month,
    CONCAT(u.first_name, ' ', u.last_name) AS driver,
    COUNT(*) AS "Count of Trips > 1 hr"
FROM
    RideDurations rd
JOIN
    users_user u ON rd.id_driver = u.id_user
WHERE
    dropoff_time - pickup_time > INTERVAL '1 hour' -- Filter for trips > 1 hour
GROUP BY
    TO_CHAR(DATE_TRUNC('month', TO_TIMESTAMP(year || '-' || month || '-01', 'YYYY-MM-DD')), 'YYYY-MM'),
    driver
ORDER BY
    month DESC, driver;
```
