import { setupWorker, rest } from 'msw'
export const { REACT_APP_BACKEND_URL } = process.env
const worker = setupWorker(
  rest.get(`${REACT_APP_BACKEND_URL}/users`, (req, res, ctx) => {
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
  })
)

worker.start()
