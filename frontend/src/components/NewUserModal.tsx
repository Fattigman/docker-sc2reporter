import React, { useState } from 'react'
import { Button, Form, Input, Modal, Result, Select } from 'antd'
import { UserAddOutlined } from '@ant-design/icons'
import { addUser } from '../services/api'
import { scopes } from '../services/costants'

export const NewUserModal = ({ updateUsers, token }) => {
  const [isModalVisible, setIsModalVisible] = useState<boolean>(false)
  const [isRegistrationSuccessful, setIsRegistrationSuccessful] = useState<boolean>(false)

  const showModal = () => {
    setIsModalVisible(true)
  }

  const registerUser = (user) => {
    addUser(token, user).then(() => {
      updateUsers()
      setIsRegistrationSuccessful(true)
    })
  }

  const handleCancel = () => {
    setIsModalVisible(false)
    setIsRegistrationSuccessful(false)
  }
  return (
    <>
      <Button type={'primary'} onClick={showModal}>
        <UserAddOutlined style={{ fontSize: '20px' }} />
      </Button>
      <Modal title="Add new user" visible={isModalVisible} footer={null} onCancel={handleCancel}>
        {!isRegistrationSuccessful && (
          <Form name="basic" onFinish={registerUser} autoComplete="off">
            <Form.Item
              name="email"
              rules={[
                {
                  required: true,
                  message: 'Please input an email',
                  type: 'email',
                },
              ]}
            >
              <Input placeholder="Email" />
            </Form.Item>
            <Form.Item
              name="fullname"
              rules={[
                {
                  required: true,
                  message: `Please input the user's full name`,
                },
              ]}
            >
              <Input placeholder="Full name" />
            </Form.Item>
            <Form.Item
              name="username"
              rules={[
                {
                  required: true,
                  message: `Please input a username`,
                },
              ]}
            >
              <Input placeholder="Username" />
            </Form.Item>
            <Form.Item name="scope">
              <Select defaultValue={Object.keys(scopes)[0]}>
                {Object.keys(scopes).map((scope) => (
                  <Select.Option key={scope} value={scope}>
                    {scope}
                  </Select.Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item
              name="password"
              rules={[
                {
                  required: true,
                  message: `Please input a password`,
                },
              ]}
            >
              <Input placeholder="Password" />
            </Form.Item>
            <Form.Item>
              <Button htmlType="submit" type={'primary'}>
                Add user
              </Button>
            </Form.Item>
          </Form>
        )}
        {isRegistrationSuccessful && (
          <div>
            <Result status="success" title="New user added!" />
          </div>
        )}
      </Modal>
    </>
  )
}
