# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-06-03 18:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0056_convert_strike_jobs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobexecution',
            name='command_arguments',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='cpus_scheduled',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='disk_out_scheduled',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='disk_total_scheduled',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='ended',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='environment',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='error',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='job_completed',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='job_exit_code',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='job_metrics',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='job_started',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='last_modified',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='mem_scheduled',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='post_completed',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='post_exit_code',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='post_started',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='pre_completed',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='pre_exit_code',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='pre_started',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='results',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='results_manifest',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='status',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='stderr',
        ),
        migrations.RemoveField(
            model_name='jobexecution',
            name='stdout',
        ),
        migrations.AlterIndexTogether(
            name='jobexecution',
            index_together=set([]),
        ),
        migrations.AlterIndexTogether(
            name='jobexecutionend',
            index_together=set([]),
        ),
        migrations.AlterIndexTogether(
            name='jobexecutionoutput',
            index_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='jobexecution',
            unique_together=set([('job', 'exe_num')]),
        ),
        migrations.AlterUniqueTogether(
            name='jobexecutionend',
            unique_together=set([('job', 'exe_num')]),
        ),
        migrations.AlterUniqueTogether(
            name='jobexecutionoutput',
            unique_together=set([('job', 'exe_num')]),
        ),
    ]
