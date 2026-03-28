## Bone Age Estimation Frontend

This folder contains a small, professional React frontend that talks to your existing FastAPI backend defined in `app.py`.

### Tech stack

- **React 18** with **TypeScript**
- **Vite** for fast dev/build
- **Tailwind CSS** for styling

### API contract

The UI is wired to the FastAPI endpoint:

- **POST** `/predict`
  - `multipart/form-data`
  - Fields:
    - `image`: uploaded X-ray image file
    - `patient_id`: string
  - Returns a JSON payload compatible with the response from `app.py` (male and female predictions, Grad-CAM URLs, etc.).

During development, Vite proxies frontend calls from `/api` to `http://localhost:8000` (see `vite.config.ts`), so the React code calls:

- `POST /api/predict` → `http://localhost:8000/predict`
- Grad-CAM images: `GET /api/storage/...` → `http://localhost:8000/storage/...`

Make sure your FastAPI app is running on port **8000**.

### Running locally

From the `frontend` directory:

```bash
npm install
npm run dev
```

Then open the printed Vite dev URL (default `http://localhost:5173`).

### Build for production

```bash
npm run build
```

The static assets will be output to `dist/`. You can then serve them with any static file server or integrate into your deployment pipeline alongside the FastAPI backend.

