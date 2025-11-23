"""
EC2 Models Module - Provides data models for EC2 operations.

This module defines Pydantic models for EC2 instance filtering, start/stop requests,
creation requests, and instance representation for use with the OpenAI Agents SDK.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, model_serializer


class EC2InstanceFilter(BaseModel):
    """
    Filter parameters for listing EC2 instances.
    """
    
    region: str = Field(
        description="AWS region to filter instances by"
    )
    
    instance_ids: Optional[List[str]] = Field(
        default=None,
        description="List of specific instance IDs to filter by"
    )
    
    state: Optional[str] = Field(
        default=None,
        description="Instance state to filter by (e.g., 'running', 'stopped')"
    )
    
    instance_type: Optional[str] = Field(
        default=None,
        description="Instance type to filter by (e.g., 't2.micro')"
    )
    
    tag_key: Optional[str] = Field(
        default=None,
        description="Tag key to filter by"
    )
    
    tag_value: Optional[str] = Field(
        default=None,
        description="Tag value to filter by"
    )
    
    def to_aws_filters(self) -> List[Dict[str, Any]]:
        """
        Convert the filter to AWS API format.
        
        Returns:
            List of AWS filter dictionaries
        """
        filters = []
        
        if self.state:
            filters.append({
                'Name': 'instance-state-name',
                'Values': [self.state]
            })
            
        if self.instance_type:
            filters.append({
                'Name': 'instance-type',
                'Values': [self.instance_type]
            })
            
        if self.tag_key and self.tag_value:
            filters.append({
                'Name': f'tag:{self.tag_key}',
                'Values': [self.tag_value]
            })
                
        return filters


class EC2StartStopRequest(BaseModel):
    """
    Request model for starting or stopping EC2 instances.
    """
    
    instance_ids: List[str] = Field(
        description="List of instance IDs to start or stop"
    )
    
    region: str = Field(
        description="AWS region where the instances are located"
    )
    
    force: bool = Field(
        default=False,
        description="Whether to force stop the instances (only applicable for stopping)"
    )


class EC2CreateRequest(BaseModel):
    """
    Request model for creating a new EC2 instance.
    """
    
    image_id: str = Field(
        description="AMI ID to use for the instance"
    )
    
    instance_type: str = Field(
        description="Instance type (e.g., 't2.micro')"
    )
    
    region: str = Field(
        description="AWS region to create the instance in"
    )
    
    key_name: Optional[str] = Field(
        default=None,
        description="Name of the key pair to use for SSH access"
    )
    
    security_group_ids: Optional[List[str]] = Field(
        default=None,
        description="List of security group IDs to associate with the instance"
    )
    
    subnet_id: Optional[str] = Field(
        default=None,
        description="ID of the subnet to launch the instance in"
    )
    
    user_data: Optional[str] = Field(
        default=None,
        description="User data script to run on instance launch"
    )
    
    tag_name: Optional[str] = Field(
        default=None,
        description="Name tag for the instance"
    )
    
    tag_environment: Optional[str] = Field(
        default=None,
        description="Environment tag for the instance (e.g., 'dev', 'prod')"
    )
    
    tag_owner: Optional[str] = Field(
        default=None,
        description="Owner tag for the instance"
    )
    
    iam_instance_profile: Optional[str] = Field(
        default=None,
        description="IAM instance profile name or ARN"
    )
    
    ebs_optimized: bool = Field(
        default=False,
        description="Whether the instance is EBS optimized"
    )
    
    instance_initiated_shutdown_behavior: Optional[str] = Field(
        default=None,
        description="Instance behavior on shutdown ('stop' or 'terminate')"
    )


class EC2Instance(BaseModel):
    """
    Model representing an EC2 instance.
    """
    
    instance_id: str = Field(
        description="Unique identifier for the EC2 instance"
    )
    
    state: str = Field(
        description="Current state of the instance (e.g., 'running', 'stopped')"
    )
    
    instance_type: str = Field(
        description="Type of the instance (e.g., 't2.micro')"
    )
    
    public_ip_address: Optional[str] = Field(
        default=None,
        description="Public IP address of the instance"
    )
    
    private_ip_address: Optional[str] = Field(
        default=None,
        description="Private IP address of the instance"
    )
    
    tag_name: Optional[str] = Field(
        default=None,
        description="Name tag of the instance"
    )
    
    tag_environment: Optional[str] = Field(
        default=None,
        description="Environment tag of the instance"
    )
    
    tag_owner: Optional[str] = Field(
        default=None,
        description="Owner tag of the instance"
    )
    
    launch_time: Optional[str] = Field(
        default=None,
        description="Time when the instance was launched"
    )
    
    availability_zone: Optional[str] = Field(
        default=None,
        description="Availability zone where the instance is located"
    )
    
    vpc_id: Optional[str] = Field(
        default=None,
        description="ID of the VPC where the instance is located"
    )
    
    subnet_id: Optional[str] = Field(
        default=None,
        description="ID of the subnet where the instance is located"
    )
    
    security_group_ids: Optional[List[str]] = Field(
        default=None,
        description="Security group IDs associated with the instance"
    )
    
    security_group_names: Optional[List[str]] = Field(
        default=None,
        description="Security group names associated with the instance"
    )
    
    @classmethod
    def from_aws_instance(cls, instance: Dict[str, Any]) -> 'EC2Instance':
        """
        Create an EC2Instance from AWS API response.
        
        Args:
            instance: AWS EC2 instance dictionary
            
        Returns:
            EC2Instance model
        """
        # Extract tags
        tags_dict = {}
        for tag in instance.get('Tags', []):
            tags_dict[tag.get('Key')] = tag.get('Value')
        
        # Extract security groups
        security_groups = instance.get('SecurityGroups', [])
        sg_ids = [sg.get('GroupId') for sg in security_groups if sg.get('GroupId')]
        sg_names = [sg.get('GroupName') for sg in security_groups if sg.get('GroupName')]
            
        # Create instance
        return cls(
            instance_id=instance.get('InstanceId'),
            state=instance.get('State', {}).get('Name'),
            instance_type=instance.get('InstanceType'),
            public_ip_address=instance.get('PublicIpAddress'),
            private_ip_address=instance.get('PrivateIpAddress'),
            tag_name=tags_dict.get('Name'),
            tag_environment=tags_dict.get('Environment'),
            tag_owner=tags_dict.get('Owner'),
            launch_time=instance.get('LaunchTime').isoformat() if instance.get('LaunchTime') else None,
            availability_zone=instance.get('Placement', {}).get('AvailabilityZone'),
            vpc_id=instance.get('VpcId'),
            subnet_id=instance.get('SubnetId'),
            security_group_ids=sg_ids if sg_ids else None,
            security_group_names=sg_names if sg_names else None
        )