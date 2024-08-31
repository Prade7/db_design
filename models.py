from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Custom UserManager for creating User and Superuser
class UserManager(BaseUserManager):
    def create_user(self, employee_id, password=None, **extra_fields):
        if not employee_id:
            raise ValueError("The employee_id must be set")
        user = self.model(employee_id=employee_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, employee_id, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(employee_id, password, **extra_fields)

# Custom User model
class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    employee_id = models.CharField(max_length=50, unique=True)  # Unique identifier for each user
    password_hash = models.CharField(max_length=128)  # Password stored as a hash
    role = models.CharField(max_length=50)  # Role can be Manager, Supervisor, Operator
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the user is created

    objects = UserManager()

    USERNAME_FIELD = 'employee_id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.employee_id

# Model for storing unique machine names
class MachineName(models.Model):
    machine_name = models.CharField(max_length=50, unique=True)  # Unique machine name
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='machines')
    # ForeignKey establishes a many-to-one relationship with User
    # Each user can manage multiple machines

    def __str__(self):
        return self.machine_name

# Model for storing machine details; multiple details can be associated with a single machine name
class MachineDetails(models.Model):
    machine_name = models.ForeignKey(MachineName, on_delete=models.CASCADE, related_name='details')
    # ForeignKey establishes a many-to-one relationship with MachineName

    feedrate = models.FloatField(default=0.0)
    max_acceleration = models.FloatField(default=0.0)
    max_velocity = models.FloatField(default=0.0)
    acceleration = models.FloatField(default=0.0)
    angular_units = models.FloatField(default=0.0)
    velocity = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.machine_name.machine_name}"

# Model for defining types of axes (e.g., X, Y, Z, A, B , E , F , G , H)
class AxisType(models.Model):
    name = models.CharField(max_length=5, unique=True)  # Axis name, such as 'X', 'Y', 'Z' , 'A' , 'B'
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='machines')
    # ForeignKey establishes a many-to-one relationship with User
    def __str__(self):
        return self.name

# Model for storing axis details; multiple axes can be associated with a single machine detail
class Axis(models.Model):
    axis_type = models.ForeignKey(AxisType, on_delete=models.CASCADE, related_name='axes')
    # ForeignKey establishes a many-to-one relationship with AxisType
   
    machine = models.ForeignKey(MachineDetails, on_delete=models.CASCADE, related_name='axes')
    # ForeignKey establishes a many-to-one relationship with MachineDetails

    actual_position = models.FloatField(default=0.0)  
    distance_to_go = models.FloatField(default=0.0)   
    tool_offset = models.FloatField(default=0.0)      
    homed = models.BooleanField(default=True)         # Boolean to check if the axis is homed
    timestamp = models.DateTimeField(auto_now=True)  # Auto-updated timestamp for each record

    def __str__(self):
        return f"Axis {self.axis_type.name} of Machine {self.machine}"
