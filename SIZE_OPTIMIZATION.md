# Size Optimization for Vercel

## Changes Made to Reduce Deployment Size

### 1. Removed Unused Dependencies
- **axios** - Not used, code uses native `fetch()` API (saves ~50MB)

### 2. Created .vercelignore Files
- Root `.vercelignore` - Excludes large directories from deployment
- `frontend/.vercelignore` - Excludes frontend-specific large files

### 3. Next.js Build Optimizations
- Added `swcMinify: true` for faster, smaller builds
- Added `compress: true` for gzip compression
- Excluded platform-specific SWC binaries from build
- Excluded esbuild binaries (not needed in production)

### 4. Excluded Directories
The following are excluded from Vercel deployment:
- `node_modules/` - Installed by Vercel automatically
- `.next/` - Built by Vercel during deployment
- `uploads/` - User-generated content (use external storage)
- `data/` - JSON database files (use external storage in production)
- `__pycache__/` - Python cache files
- `.git/` - Git repository
- Build artifacts and logs

## Expected Size Reduction

- **Removed axios dependency**: ~50MB
- **Excluded directories** (node_modules, .next, uploads, data, etc.): ~150-200MB
- **Build optimizations** (excluded SWC/esbuild binaries): ~30-50MB

**Total expected reduction**: ~230-300MB

**Note**: Vercel automatically installs `node_modules` during build, so excluding it from the zip file is crucial.

## Important Notes

1. **Data Storage**: The `data/` directory is excluded. For production, use:
   - Vercel KV (Redis)
   - External database (PostgreSQL, MongoDB)
   - Vercel Blob Storage

2. **File Uploads**: The `uploads/` directory is excluded. Use:
   - Vercel Blob Storage
   - AWS S3
   - Cloudinary

3. **Environment Variables**: Make sure to set:
   - `NEXT_PUBLIC_API_URL` - Your backend API URL
   - `FRONTEND_URL` - Your frontend URL (for CORS)

## Deployment Checklist

- [ ] Remove `node_modules` before zipping (Vercel installs them)
- [ ] Ensure `.vercelignore` is in place
- [ ] Verify `data/` and `uploads/` are excluded
- [ ] Set up external storage for production data
- [ ] Configure environment variables in Vercel dashboard

