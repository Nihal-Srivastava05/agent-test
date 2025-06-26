# 🚀 GitHub Pages Deployment Guide

This guide will help you deploy your AgentTest documentation to GitHub Pages using the automated GitHub Actions workflow.

## 📋 Prerequisites

- GitHub repository with the AgentTest code
- Admin access to the repository
- Documentation files in the `docs/` directory
- Updated GitHub Actions workflow (`.github/workflows/docs.yml`)

## 🔧 Step-by-Step Setup

### Step 1: Update Repository URLs

Before deploying, update the repository URLs in `mkdocs.yml` to match your actual repository:

```yaml
# Update these lines in mkdocs.yml
site_url: https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/
repo_name: YOUR-USERNAME/YOUR-REPO-NAME
repo_url: https://github.com/YOUR-USERNAME/YOUR-REPO-NAME
```

For example, if your GitHub username is `johndoe` and repository is `agent-test`:

```yaml
site_url: https://johndoe.github.io/agent-test/
repo_name: johndoe/agent-test
repo_url: https://github.com/johndoe/agent-test
```

Also update the social links:

```yaml
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/YOUR-USERNAME/YOUR-REPO-NAME
    - icon: fontawesome/brands/python
      link: https://pypi.org/project/agenttest/ # Update if you have a different package name
```

And the magic link configuration:

```yaml
- pymdownx.magiclink:
    normalize_issue_symbols: true
    repo_url_shorthand: true
    user: YOUR-USERNAME
    repo: YOUR-REPO-NAME
```

### Step 2: Enable GitHub Pages

1. **Go to Repository Settings**:

   - Navigate to your repository on GitHub
   - Click on the "Settings" tab

2. **Configure Pages**:
   - Scroll down to "Pages" in the left sidebar
   - Under "Source", select **"GitHub Actions"**
   - Click "Save"

### Step 3: Set Repository Permissions

1. **Go to Actions Settings**:
   - In repository settings, click "Actions" → "General"
   - Under "Workflow permissions", select **"Read and write permissions"**
   - Check **"Allow GitHub Actions to create and approve pull requests"**
   - Click "Save"

### Step 4: Add Repository Secrets (Optional)

For Google Analytics tracking:

1. **Go to Repository Secrets**:

   - Settings → Secrets and variables → Actions
   - Click "New repository secret"

2. **Add Google Analytics**:
   - Name: `GOOGLE_ANALYTICS_KEY`
   - Value: Your Google Analytics measurement ID (e.g., `G-XXXXXXXXXX`)

### Step 5: Commit and Push Changes

```bash
# Add all the new files
git add .

# Commit the changes
git commit -m "Add MkDocs documentation and GitHub Pages deployment"

# Push to main branch
git push origin main
```

### Step 6: Monitor Deployment

1. **Check Actions Tab**:

   - Go to the "Actions" tab in your repository
   - You should see a workflow run for "Build and Deploy Documentation"
   - Click on it to monitor progress

2. **Wait for Completion**:

   - The build job should complete in 2-3 minutes
   - The deploy job will run after build succeeds

3. **Access Your Documentation**:
   - Once deployed, visit: `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/`
   - It may take a few minutes for the site to be available

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. Build Fails with "Module not found"

**Error**: `ModuleNotFoundError: No module named 'mkdocs'`

**Solution**: The workflow should install dependencies automatically. If it fails:

- Check that `pyproject.toml` includes the `docs` extras
- Verify the workflow file has the correct installation command

#### 2. Site URL Issues

**Error**: Links or styling broken on the deployed site

**Solution**:

- Ensure `site_url` in `mkdocs.yml` matches your actual GitHub Pages URL
- Use relative paths in documentation links

#### 3. Permission Denied

**Error**: `Error: Resource not accessible by integration`

**Solution**:

- Check repository permissions in Settings → Actions → General
- Ensure "Read and write permissions" is selected

#### 4. Pages Not Updating

**Issue**: Changes not reflected on the live site

**Solution**:

- Check if the GitHub Actions workflow completed successfully
- Try a hard refresh (Ctrl+F5 or Cmd+Shift+R)
- Check if there are any caching issues

#### 5. 404 Error on GitHub Pages

**Issue**: GitHub Pages shows 404 error

**Solution**:

- Verify GitHub Pages is configured to use "GitHub Actions" as source
- Check that the workflow uploaded the artifact correctly
- Ensure the `site/` directory was built properly

### Debug Commands

Run these locally to test before pushing:

```bash
# Test build locally
./scripts/docs.sh build-strict

# Check for broken links
./scripts/docs.sh check-links

# Serve locally to test
./scripts/docs.sh serve
```

## 🎯 Advanced Configuration

### Custom Domain (Optional)

To use a custom domain:

1. **Add CNAME file**:

   ```bash
   echo "docs.yourdomain.com" > docs/CNAME
   ```

2. **Update site_url**:

   ```yaml
   site_url: https://docs.yourdomain.com/
   ```

3. **Configure DNS**:
   - Add a CNAME record pointing to `YOUR-USERNAME.github.io`

### Branch Protection

To ensure documentation quality:

1. **Enable branch protection** for `main` branch
2. **Require status checks** including the documentation build
3. **Require pull request reviews** for documentation changes

### Automated Updates

The workflow triggers on:

- Push to `main` branch (deploys automatically)
- Pull requests (builds for testing, doesn't deploy)
- Changes to documentation files, `mkdocs.yml`, or workflow files

## 📈 Monitoring and Analytics

### GitHub Actions Insights

- Monitor deployment frequency and success rate
- Check build times and optimize if needed

### Google Analytics (if configured)

- Track documentation usage
- Identify popular pages
- Monitor user engagement

### GitHub Pages Analytics

- Check repository insights for traffic data
- Monitor referrers and popular content

## 🔄 Maintenance

### Regular Updates

- Keep MkDocs and plugins updated in `pyproject.toml`
- Update GitHub Actions to latest versions
- Review and update documentation content

### Performance Optimization

- Optimize images in `docs/images/`
- Minimize custom CSS/JS
- Use MkDocs minify plugin (already configured)

## 📞 Support

If you encounter issues:

1. **Check the workflow logs** in the Actions tab
2. **Review this guide** for common solutions
3. **Test locally** using `./scripts/docs.sh`
4. **Open an issue** in the repository if problems persist

---

**🎉 Congratulations!** Your documentation should now be live at `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/`
