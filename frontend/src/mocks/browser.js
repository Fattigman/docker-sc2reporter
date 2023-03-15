import { setupWorker, rest } from 'msw'

export const { REACT_APP_BACKEND_URL } = process.env

const endpoints = {
  samples: 'samples/',
  samplesNextclade: `samples/nextclade/?nextclade=testNextclade`,
  samplesPango: `samples/pango/?pangolin=testPangolin`,
  variants: `variants/?variant=testVariant`,
  dashboard: `dashboard/?testSelectionCriterion`,
  samplesById: `samples/sc2-1001`,
  users: 'users/',
  getUserInfo: 'users/me/',
  usersDelete: `users/delete/?user=testUsername`,
  phyllogeny: `phyllogeny/?group=group&samples`,
}

const worker = setupWorker(
  rest.get(`${REACT_APP_BACKEND_URL}/${endpoints.phyllogeny}`, (req, res, ctx) => {
    const statusCode = 500
    if (statusCode === 401) {
      return res(ctx.status(401), ctx.json({ message: 'Unauthorized' }))
    } else if (statusCode === 404) {
      return res(ctx.status(404), ctx.json({ message: 'Not found' }))
    } else {
      return res(ctx.status(500), ctx.json({ message: 'Internal server error' }))
    }
  })
)

worker.start()
