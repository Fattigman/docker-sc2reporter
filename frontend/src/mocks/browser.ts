import { setupWorker, rest } from 'msw'

const { REACT_APP_BACKEND_URL } = process.env

const getEndpoints = {
  doNotInterrupt: 'doNotInterrupt',
  samples: 'samples/',
  samplesNextclade: `samples/nextclade/?nextclade=testNextclade`,
  samplesPango: `samples/pango/?pangolin=testPangolin`,
  variants: `variants/?variant=testVariant`,
  dashboard: `dashboard/?testSelectionCriterion`,
  sample: `samples/sc2-1001`,
  users: 'users/',
  getUserInfo: 'users/me/',
  usersDelete: `users/delete/?user=testUsername`,
  phyllogeny: `phyllogeny/?group=group&samples`,
}

const postEndpoints = {
  doNotInterrupt: 'doNotInterrupt',
  addUser: 'users/add/',
  getToken: 'login/token',
}

const deleteEndpoints = {
  doNotInterrupt: 'doNotInterrupt',
  deleteUser: 'users/delete/?user=username',
  deleteSample: 'samples/?sample_ids',
}

const worker = setupWorker(
  rest.get(`${REACT_APP_BACKEND_URL}/${getEndpoints.sample}`, (req, res, ctx) => {
    const statusCode = 409 as number
    if (statusCode === 401) {
      return res(ctx.status(401), ctx.json({ message: 'Unauthorized' }))
    } else if (statusCode === 404) {
      return res(ctx.status(404), ctx.json({ message: 'Not found' }))
    } else if (statusCode === 409) {
      return res(ctx.status(409), ctx.json({ message: "Sample can't be found in database" }))
    } else {
      return res(ctx.status(500), ctx.json({ message: 'Internal server error' }))
    }
  }),

  rest.post(`${REACT_APP_BACKEND_URL}/${postEndpoints.doNotInterrupt}`, (req, res, ctx) => {
    const statusCode = 500 as number
    if (statusCode === 401) {
      return res(ctx.status(401), ctx.json({ message: 'Unauthorized' }))
    } else if (statusCode === 404) {
      return res(ctx.status(404), ctx.json({ message: 'Not found' }))
    } else if (statusCode === 409) {
      return res(ctx.status(409), ctx.json({ message: "Sample can't be found in database" }))
    } else {
      return res(ctx.status(500), ctx.json({ message: 'Internal server error' }))
    }
  }),

  rest.delete(`${REACT_APP_BACKEND_URL}/${deleteEndpoints.doNotInterrupt}`, (req, res, ctx) => {
    const statusCode = 500 as number
    if (statusCode === 401) {
      return res(ctx.status(401), ctx.json({ message: 'Unauthorized' }))
    } else if (statusCode === 404) {
      return res(ctx.status(404), ctx.json({ message: 'Not found' }))
    } else if (statusCode === 409) {
      return res(ctx.status(409), ctx.json({ message: "Sample can't be found in database" }))
    } else {
      return res(ctx.status(500), ctx.json({ message: 'Internal server error' }))
    }
  })
)

worker.start()
