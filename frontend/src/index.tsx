import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import reportWebVitals from './reportWebVitals'
import { App } from './App'
import { BrowserRouter } from 'react-router-dom'
import ErrorBoundary from 'components/ErrorBoundary'
import { Button, Result } from 'antd'

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement)
const { REACT_APP_PREFIX_URL } = process.env

root.render(
  <React.StrictMode>
    <BrowserRouter basename={REACT_APP_PREFIX_URL}>
      <ErrorBoundary
        fallback={
          <Result
            status="warning"
            title="Something went wrong"
            subTitle="If this issue persists please contact us by adding a new issue in GitHub"
            extra={
              <Button
                type="primary"
                href="https://github.com/genomic-medicine-sweden/docker-sc2reporter/issues"
              >
                Go to GitHub
              </Button>
            }
          />
        }
      >
        <App />
      </ErrorBoundary>
    </BrowserRouter>
  </React.StrictMode>
)

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals()
