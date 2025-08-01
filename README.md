# Lubezki

Hey this projects aims to help users practice film composition and lighting (lost arts). It will have two main functionns:
1) Provide real-time concise image feedback during the framing process.
2) Give comprehensive image (and eventually video) feedback after frame has been shot.

## Roadmap

- [ ] Process images with gemini api for concise composition output
- [ ] Integrate bounding boxes and link with corresponding text data
- [ ] Get real time feedback with in-camera integration
- [ ] Set up DBs, check security, incorporate auth
- [ ] Build iOS UI
- [ ] Test
- [ ] Publish

## Project Structure

```
film-composition-ai/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/v1/endpoints/  # API endpoints
│   │   ├── core/              # Configuration and database
│   │   ├── models/            # SQL models (future)
│   │   ├── schemas/           # Pydantic schemas (future)
│   │   ├── services/          # Business logic
│   │   └── utils/             # Utility functions
│   ├── run.py                 # Development server
├── frontend-swift/            # Swift frontend (future)
├── assets/                    # Static assets
└── docs/                      # API documentation (future)
```

## More thoughtful readme pending
