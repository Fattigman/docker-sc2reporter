import React from 'react'
import { Button, Result } from 'antd'
import { Link } from 'react-router-dom'

export const ErrorPage = () => {
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
}
