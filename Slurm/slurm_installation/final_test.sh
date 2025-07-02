#!/bin/bash
#SBATCH --job-name=final_test
#SBATCH --output=logs/slurm_output/final_%j.out
#SBATCH --time=00:01:00
#SBATCH --nodes=1

echo "Final verification job - Native Slurm"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $(hostname)"
echo "Time: $(date)"
echo "✅ Native Slurm working correctly!"
