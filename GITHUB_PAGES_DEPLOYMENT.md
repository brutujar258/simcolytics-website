# GitHub Pages Deployment Guide for Simcolytics

## 🚀 Complete Step-by-Step Instructions

### Step 1: Create GitHub Repository

1. **Go to GitHub.com** and sign in to your account
2. **Click the "+" icon** in the top right corner
3. **Select "New repository"**
4. **Repository settings:**
   - **Repository name**: `simcolytics` (or `simcolytics-website`)
   - **Description**: "Professional website for Simcolytics - Where Energy meets Intelligence"
   - **Visibility**: **Public** (required for free GitHub Pages)
   - **Initialize with**: Check "Add a README file"
5. **Click "Create repository"**

### Step 2: Upload Website Files

#### Option A: Using GitHub Web Interface (Recommended for beginners)

1. **In your new repository**, click the **"Add file"** button
2. **Select "Upload files"**
3. **Drag and drop ALL files** from the `simcolytics_site` folder:
   - `index.html`
   - `styles.css`
   - `script.js`
   - `logo_draft_v3.png`
   - `favicon.svg`
   - `CNAME`
   - `404.html`
   - `robots.txt`
   - `sitemap.xml`
   - `README.md`
   - `rotating_images/` folder (with all image files)
4. **Add commit message**: "Initial website upload"
5. **Click "Commit changes"**

#### Option B: Using Git Commands (For advanced users)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/simcolytics.git
cd simcolytics

# Copy all files from simcolytics_site folder to this directory
# (Copy all files manually)

# Add all files
git add .

# Commit changes
git commit -m "Initial website upload"

# Push to GitHub
git push origin main
```

### Step 3: Enable GitHub Pages

1. **Go to your repository** on GitHub
2. **Click "Settings"** tab
3. **Scroll down to "Pages"** section (in the left sidebar)
4. **Under "Source"**, select **"Deploy from a branch"**
5. **Under "Branch"**, select **"main"** and **"/ (root)"**
6. **Click "Save"**
7. **Wait 2-5 minutes** for the site to deploy

### Step 4: Configure Custom Domain

1. **In the same "Pages" settings section**
2. **Under "Custom domain"**, enter: `simcolytics.com`
3. **Check "Enforce HTTPS"** (recommended)
4. **Click "Save"**
5. **Wait for DNS verification** (can take up to 24 hours)

### Step 5: Configure GoDaddy DNS

1. **Log into your GoDaddy account**
2. **Go to "My Products"** → **"Domains"**
3. **Find simcolytics.com** and click **"DNS"**
4. **Add these DNS records:**

#### A Records (for root domain):
```
Type: A
Name: @
Value: 185.199.108.153
TTL: 600

Type: A
Name: @
Value: 185.199.109.153
TTL: 600

Type: A
Name: @
Value: 185.199.110.153
TTL: 600

Type: A
Name: @
Value: 185.199.111.153
TTL: 600
```

#### CNAME Record (for www subdomain):
```
Type: CNAME
Name: www
Value: YOUR_USERNAME.github.io
TTL: 600
```

### Step 6: Verify Setup

1. **Check GitHub Pages status** in repository settings
2. **Test the website** at both URLs:
   - https://simcolytics.com
   - https://YOUR_USERNAME.github.io
3. **Verify SSL certificate** is working (green lock icon)

## ✅ Verification Checklist

- [ ] Repository is public
- [ ] All files uploaded correctly
- [ ] GitHub Pages enabled
- [ ] Custom domain configured
- [ ] DNS records added to GoDaddy
- [ ] SSL certificate working
- [ ] Website loads at simcolytics.com
- [ ] All links and forms working
- [ ] Mobile responsive design working
- [ ] Logo displays correctly
- [ ] Rotating images work properly
- [ ] All service cards display correctly
- [ ] Contact form functions properly

## 🔧 Troubleshooting

### Common Issues:

1. **"Page not found" error:**
   - Check that all files are in the root directory
   - Verify index.html exists
   - Wait 5-10 minutes for deployment

2. **Custom domain not working:**
   - Verify DNS records are correct
   - Wait up to 24 hours for DNS propagation
   - Check GoDaddy DNS settings

3. **SSL certificate issues:**
   - Ensure "Enforce HTTPS" is checked
   - Wait for certificate to be issued (can take 24 hours)

4. **Images not loading:**
   - Check file paths are correct
   - Verify all image files are uploaded
   - Ensure rotating_images folder contains all 4 images:
     - matthew-henry-yETqkLnhsUI-unsplash.jpg
     - sungrow-emea-itv-MC5S6cU-unsplash.jpg
     - soren-h-omfN1pW-n2Y-unsplash.jpg
     - nw_flow.jpg

5. **Logo not displaying:**
   - Verify logo_draft_v3.png is uploaded
   - Check file name matches exactly (case-sensitive)

## 📞 Support

If you encounter issues:

1. **Check GitHub Pages documentation**: https://pages.github.com/
2. **Verify DNS settings** with GoDaddy support
3. **Contact GitHub support** for Pages-specific issues
4. **Email**: simcolytics@gmail.com for website-specific questions

## 🎉 Success!

Once everything is working:
- Your site will be live at https://simcolytics.com
- Updates are automatic when you push changes to GitHub
- Free SSL certificate included
- Global CDN for fast loading worldwide

---

*Your professional Simcolytics website - Where Energy meets Intelligence - is now live and ready to attract clients!* 