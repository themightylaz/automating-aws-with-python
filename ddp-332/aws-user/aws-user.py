import boto3
import click

session = boto3.Session(profile_name='pt-operator')
s3 = session.resource('s3')


@click.group()
def cli():
    "aws-user manages AWS temporary users for firefighter access."
    pass


@cli.command('list-buckets')
def list_buckets():
    "List all s3 buckets."
    for bucket in s3.buckets.all():
        print (bucket)


if __name__ == '__main__':
    cli()
