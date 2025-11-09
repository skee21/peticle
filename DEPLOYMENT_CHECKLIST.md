# Vercel Deployment Checklist

## Before Zipping/Uploading

### 1. Remove Large Directories
Before creating your deployment package, ensure these are excluded:

```bash
# These should NOT be in your zip file:
- node_modules/          # Vercel installs automatically
- frontend/node_modules/ # Vercel installs automatically  
- .next/                 # Built by Vercel during deployment
- frontend/.next/        # Built by Vercel during deployment
- data/                   # Use external storage
- uploads/               # Use external storage
- __pycache__/           # Python cache
- .git/                  # Git repository
```

### 2. Verify .vercelignore Files
- ✅ Root `.vercelignore` exists
- ✅ `frontend/.vercelignore` exists
- ✅ Both exclude `node_modules`, `.next`, `data`, `uploads`

### 3. Check Package Size
After excluding the above, your zip should be:
- **Target**: < 250MB (Vercel limit)
- **Expected**: ~50-100MB (source code only)

## Deployment Steps

### Backend (FastAPI)
1. Set root directory to project root
2. Vercel will use `vercel.json` configuration
3. Ensure `requirements.txt` is in root
4. Set environment variables:
   - `FRONTEND_URL`
   - `OPENAI_API_KEY` (optional)
   - `GOOGLE_MAPS_API_KEY` (optional)

### Frontend (Next.js)
1. Set root directory to `frontend/`
2. Vercel will auto-detect Next.js
3. Set environment variables:
   - `NEXT_PUBLIC_API_URL` - Your backend API URL

## Size Optimization Summary

| Item | Size Saved |
|------|------------|
| Removed axios | ~50MB |
| Excluded node_modules | ~150-200MB |
| Excluded .next build | ~50-100MB |
| Excluded data/uploads | ~10-50MB |
| Build optimizations | ~30-50MB |
| **Total** | **~290-450MB** |

## Important Notes

1. **Vercel installs dependencies automatically** - Don't include `node_modules` in zip
2. **Vercel builds Next.js** - Don't include `.next` folder
3. **Use external storage** for `data/` and `uploads/` in production
4. **Environment variables** must be set in Vercel dashboard

## Troubleshooting

### Still over 250MB?
1. Check if `.vercelignore` is working
2. Verify `node_modules` is excluded
3. Check for large files in `uploads/` or `data/`
4. Remove any `.git/` directory
5. Check for duplicate dependencies

### Build fails?
1. Verify `requirements.txt` is in root
2. Check Python version compatibility
3. Verify all environment variables are set
4. Check Vercel build logs for errors

