#!/bin/bash
#SBATCH --job-name=cancellation_test
#SBATCH --output=cancel_%j.out
#SBATCH --time=00:10:00

echo "Job for cancellation test - Job ID: $SLURM_JOB_ID"
echo "This job should be cancelled before completion"
for i in {1..600}; do
    echo "Step $i/600 - $(date)"
    sleep 1
done
echo "ERROR: Job completed without being cancelled!"
