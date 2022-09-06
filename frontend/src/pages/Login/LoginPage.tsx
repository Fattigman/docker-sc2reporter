import * as React from 'react'
import styles from './LoginPage.module.css'
import { Form, Input, Button } from 'antd'

export const LoginPage = ({ login }) => {
  const onSubmit = (values) => {
    login(values)
  }

  const onSubmitFailed = (errorInfo) => {
    console.log('Failed:', errorInfo)
  }
  return (
    <div className={styles.homeContainer}>
      <div className={styles.loginContainer}>
        <div className={styles.form}>
          <Form name="basic" onFinish={onSubmit} onFinishFailed={onSubmitFailed} autoComplete="off">
            <Form.Item
              name="username"
              rules={[
                {
                  required: true,
                  message: 'Please input your username!',
                },
              ]}
            >
              <Input placeholder="Username" />
            </Form.Item>
            <Form.Item
              name="password"
              rules={[
                {
                  required: true,
                  message: 'Please input your password!',
                },
              ]}
            >
              <Input.Password placeholder="Password" />
            </Form.Item>
            <Form.Item>
              <Button htmlType="submit" type={'primary'}>
                Sign in
              </Button>
            </Form.Item>
          </Form>
        </div>
      </div>
    </div>
  )
}
