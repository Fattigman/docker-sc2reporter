import { setupWorker, rest } from 'msw'

export const { REACT_APP_BACKEND_URL } = process.env

const worker = setupWorker(
  rest.get(`${REACT_APP_BACKEND_URL}/users`, (req, res, ctx) => {
    const statusCode = 500
    if (statusCode === 200) {
      return res(
        ctx.json([
          {
            username: 'mock',
            email: 'mock@email.se',
            fullname: 'Mock Mock',
            disabled: false,
            scope: 'admin',
          },
        ])
      )
    } else if (statusCode === 401) {
      return res(ctx.status(401), ctx.json({ message: 'Unauthorized' }))
    } else if (statusCode === 404) {
      return res(ctx.status(404), ctx.json({ message: 'Not found' }))
    } else {
      return res(ctx.status(500), ctx.json({ message: 'Internal server error' }))
    }
  })
)

worker.start()
