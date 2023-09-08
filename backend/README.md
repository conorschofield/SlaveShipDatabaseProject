# Backend

Provides a REST interface to the database.

## Running

For a production environment, run:

```
npm run prod
```

For a development encironment, run:

```
npm run dev
```

Note that we use `nodemon` with the `-L` flag, which is needed because file watching is not available on Windows with WSL.
