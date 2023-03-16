import React from 'react'
import { Button, Result } from 'antd'
import { Link, useParams } from 'react-router-dom'

export const ErrorPage = () => {
  const errorStatus = useParams()
  switch (errorStatus.id) {
    case '404':
      return (
        <Result
          status="404"
          title="404"
          subTitle="Sorry, the page you visited does not exist."
          extra={
            <Button type="primary" key="console">
              <Link to="/">Back to Home</Link>
            </Button>
          }
        />
      )
      break
    default:
      return (
        <Result
          title={'Something went wrong'}
          extra={
            <Button type="primary" key="console">
              <Link to="/">Back to Home</Link>
            </Button>
          }
        />
      )
  }
}
