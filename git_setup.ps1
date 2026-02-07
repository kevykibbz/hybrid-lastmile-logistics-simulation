# Git Setup and Push Commands

# Navigate to project directory
cd "C:\Users\user\OneDrive\Documents\kevin\clients\Jareena\Task 1\code\hybrid_simulation"

# Initialize git repository
git init

# Add all files (respecting .gitignore)
git add .

# Check what will be committed
git status

# Commit with meaningful message
git commit -m "Initial commit: Hybrid DES+ABM urban logistics simulation

- Complete simulation framework (DES + ABM)
- Normal and peak demand scenarios
- Publication-ready visualizations
- Comprehensive documentation
- Sample outputs included"

# Add remote repository
git remote add origin https://github.com/kevykibbz/hybrid-lastmile-logistics-simulation.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main

# Verify push success
git remote -v
git log --oneline

echo "✓ Repository successfully pushed to GitHub!"
