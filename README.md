![image](https://github.com/user-attachments/assets/5e83e741-03b3-449f-a72d-bab9d20497f3)





# Machine Management System - Model Documentation


## Models


#### `User` Class

- **Purpose**: Represents users in the system, such as Managers, Supervisors, and Operators.
- **Fields**:
  - `id`: Primary key, auto-incrementing integer.
  - `employee_id`: A unique identifier for each user, such as an employee ID.
  - `password_hash`: Stores the hashed password for the user.
  - `role`: Indicates the role of the user (e.g., Manager, Supervisor, Operator).
  - `created_at`: Automatically sets the timestamp when the user is created.
- **Meta**:
  - `USERNAME_FIELD`: Uses `employee_id` as the unique identifier for authentication.
  - `REQUIRED_FIELDS`: Additional required fields for creating a user; empty in this setup.
- **Methods**:
  - `__str__`: Returns the `employee_id` for easy identification of users.

### 2. MachineName Model

- **Purpose**: Stores unique names for each machine and links each machine to a user who manages it.
- **Fields**:
  - `machine_name`: A unique name identifying the machine.
  - `user`: A foreign key linking the machine to a `User`, establishing a many-to-one relationship.
    - `on_delete=models.SET_NULL`: If the associated user is deleted, the `user` field in `MachineName` is set to `NULL`.
    - `related_name='machines'`: Allows reverse lookup from `User` to find all machines managed by that user.
- **Methods**:
  - `__str__`: Returns the machine name.

### 3. MachineDetails Model

- **Purpose**: Stores various configuration details for each machine, allowing multiple configurations for a single machine name.
- **Fields**:
  - `machine_name`: A foreign key linking each set of machine details to a `MachineName`.
    - `on_delete=models.CASCADE`: If the associated machine name is deleted, all related machine details are also deleted.
    - `related_name='details'`: Allows reverse lookup from `MachineName` to find all associated machine details.
  - `feedrate`, `max_acceleration`, `max_velocity`, `acceleration`, `angular_units`, `velocity`: Stores various operational parameters of the machine.
- **Methods**:
  - `__str__`: Returns the machine name.

### 4. AxisType Model

- **Purpose**: Defines different types of axes that can be associated with machines (e.g., 'X', 'Y', 'Z').
- **Fields**:
  - `name`: The name of the axis type, which must be unique (e.g., 'X', 'Y').
  - `user`: A foreign key linking the axis type to a `User`, indicating which user created or manages this axis type.
    - `on_delete=models.SET_NULL`: If the associated user is deleted, the `user` field is set to `NULL`.
    - `related_name='machines'`: This name seems less descriptive; consider changing to `related_name='axis_types'` for clarity.
- **Methods**:
  - `__str__`: Returns the name of the axis type.

### 5. Axis Model

- **Purpose**: Stores specific details for each axis associated with a machine's configuration.
- **Fields**:
  - `axis_type`: A foreign key linking each axis to an `AxisType`, indicating the type of axis.
    - `on_delete=models.CASCADE`: If the axis type is deleted, associated axis records are also deleted.
    - `related_name='axes'`: Allows reverse lookup from `AxisType` to its axis instances.
  - `machine`: A foreign key linking each axis to `MachineDetails`, associating it with a particular machine configuration.
    - `on_delete=models.CASCADE`: If the machine details are deleted, associated axis records are also deleted.
    - `related_name='axes'`: Allows reverse lookup from `MachineDetails` to its associated axes.
  - `actual_position`, `distance_to_go`, `tool_offset`, `homed`: Stores specific details about the axis, such as its position and whether it is homed.
  - `timestamp`: Automatically updates the timestamp when the record is modified.
- **Methods**:
  - `__str__`: Returns a string representation indicating the axis type and the associated machine.

## Relationships Summary

1. **User and MachineName**: A user can manage multiple machines, but each machine is managed by a single user.
2. **MachineName and MachineDetails**: A machine can have multiple sets of details, but each set of details is linked to one machine.
3. **User and AxisType**: Each axis type can optionally be linked to a user, indicating who created or manages it.
4. **MachineDetails and Axis**: A set of machine details can have multiple axes, each linked to a type of axis.
5. **AxisType and Axis**: Each axis is associated with one type, but a type can be used for multiple axes.

## Usage

### User Management

- Users can be created with different roles (Manager, Supervisor, Operator).
- Each user can be linked to multiple machines, indicating their responsibility.

### Machine Management

- Machines can be added with unique names and associated with a user.
- Each machine can have multiple configurations tracked via `MachineDetails`.

### Axis Management

- Different types of axes can be defined.
- Each set of machine details can have multiple axes associated with it, each axis linked to a type.

