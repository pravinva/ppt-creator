"""
Advanced PM with pyCritical - Critical Path Method (CPM)
Professional project scheduling with critical path identification
"""
from pyCritical.src.cpm_pert import critical_path_method
from PIL import Image
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

# Example: Databricks Medallion Implementation
tasks_medallion = [
    ['Discovery', [], 30],
    ['Architecture', ['Discovery'], 45],
    ['Infrastructure', ['Discovery'], 30],
    ['Bronze Layer', ['Architecture', 'Infrastructure'], 45],
    ['Silver Layer', ['Bronze Layer'], 45],
    ['Gold Layer', ['Silver Layer'], 45],
    ['Integration Test', ['Gold Layer'], 30],
    ['UAT', ['Integration Test'], 25],
    ['Deployment', ['UAT'], 15],
]

print("Running CPM Analysis on Databricks Medallion Project...")
result = critical_path_method(dataset=tasks_medallion)

print("\n📊 CPM Results:")
print(result.to_string())

# Identify critical path
critical_tasks = result[result['Slack'] == 0]
print("\n🎯 CRITICAL PATH:")
for task in critical_tasks.index:
    print(f"  → {task}")

print(f"\n📅 Total Project Duration: {result['LF'].max():.0f} days")

# Create Gantt chart
from pyCritical.src.cpm_pert import gantt_chart
fig = plt.figure(figsize=(16, 10), dpi=300)
gantt_chart(dataset=tasks_medallion, dates=result, size_x=16, size_y=10)
plt.savefig('pm_medallion_cpm.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n✅ Gantt chart saved: pm_medallion_cpm.png")
print("   • Critical path highlighted in RED")
print("   • Non-critical tasks in BLUE with slack shown")
