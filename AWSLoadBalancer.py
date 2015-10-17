
import boto.ec2.elb
import boto
import sys

AWSAccessKeyId=""
AWSSecretKey=""


class AccessLB:
    def __init__(self,AWSKeyId,AWSSecretKey,number):
        self.AWSAccessKeyId = AWSKeyId
        self.AWSSecretKey = AWSSecretKey
        self.elb_conn = boto.ec2.elb.connect_to_region("us-east-1",
                                      aws_access_key_id=AWSAccessKeyId,
                                      aws_secret_access_key=AWSSecretKey)
        self.ELB = ""
        self.Instances = ""
        self.number = number
        self.SetInstances()
    def SetInstances(self):
        if self.number == 1:
            print(self.elb_conn.get_all_load_balancers())
            self.ELB = self.elb_conn.get_all_load_balancers()[0]
            self.Instances = self.ELB.instances
        elif self.number == 2:
            self.ELB = self.elb_conn.get_all_load_balancers()[1]
            self.Instances = self.ELB.instances
    def GetInstances(self):
        print("Instances available on your ELB:")
        print(self.Instances)
    def AddInstances(self,instance_list):
        for instance_id in instance_list:
            try:
                self.elb_conn.register_instances(self.ELB.name,[instance_id])
                self.SetInstances()
                print('Adding %s to ELB %s' % (instance_id, self.ELB.name))
            except Exception as e:
                print("Something wrond on your instance")
                print(e)
    def RemoveInstances(self,instance_list):
        for instance_id in instance_list:
            if instance_id in [i.id for i in self.Instances]:
                if len(self.Instances) > 1:
                    self.elb_conn.deregister_instances(self.ELB.name,[instance_id])
                    self.SetInstances()
                    print('Removing %s from ELB %s' % (instance_id, self.ELB.name))
                else:
                    print("There is only one instance")
            else:
                print("Instance %s is not available in ELB %s" % (instance_id, self.ELB.name))
                

