#!/bin/bash
#SBATCH --job-name=comprehensive_test
#SBATCH --output=comprehensive_%j.out
#SBATCH --time=00:01:30

echo "🎯 Comprehensive MCP Capability Test"
echo "Job ID: $SLURM_JOB_ID"
echo "Job Name: $SLURM_JOB_NAME"
echo "Node: $(hostname)"
echo "User: $USER"
echo "Start Time: $(date)"
echo ""
echo "System Information:"
echo "CPUs: $(nproc)"
echo "Memory: $(free -h | grep Mem)"
echo ""
echo "Slurm Environment:"
echo "SLURM_JOB_ID: $SLURM_JOB_ID"
echo "SLURM_NTASKS: $SLURM_NTASKS"
echo "SLURM_CPUS_ON_NODE: $SLURM_CPUS_ON_NODE"
echo ""
echo "Running comprehensive test computation..."
for i in {1..10}; do
    echo "Processing step $i/10 at $(date)"
    sleep 1
done
echo ""
echo "✅ Comprehensive test completed successfully!"
echo "End Time: $(date)"
