import React, { useEffect, useState } from 'react'
import { notification, Popconfirm, Table, Tag, Tooltip } from 'antd'
import { Link } from 'react-router-dom'
import { DeleteTwoTone } from '@ant-design/icons'
import { deleteUser, getUsers } from '../../services/api'
import { NewUserModal } from '../../components/NewUserModal'
import { LoadingPage } from '../LoadingPage'

export const UserListPage = ({ token }) => {
  const [users, setUsers] = useState<any[]>()
  const [isLoading, setIsLoading] = useState<boolean>(true)

  useEffect(() => {
    updateUsersList()
  }, [])

  const updateUsersList = () => {
    getUsers(token)
      .then((response) => {
        setUsers(response)
        setIsLoading(false)
      })
      .catch(() => setIsLoading(false))
  }

  const confirmDeleteUser = (username: string) => {
    deleteUser(username).then(() => {
      notification['success']({
        message: `User deleted`,
      })
      getUsers(token).then((users) => {
        setUsers(users)
      })
    })
  }

  const columns = [
    {
      title: 'User',
      dataIndex: 'name',
      key: 'name',
      render: (name, user) => <Link to={`/genotype/users/${user.id}`}>{name}</Link>,
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: 'Id',
      dataIndex: 'id',
      key: 'id',
    },
    {
      title: 'status',
      key: 'status',
      render: ({ email }) => {
        return email[0] === '_' ? <Tag>INACTIVE</Tag> : <Tag color={'cyan'}>ACTIVE</Tag>
      },
    },
    {
      title: 'Actions',
      key: 'actions',
      render: ({ id, email }) => (
        <div style={{ display: 'flex' }}>
          <Tooltip title="Delete user">
            <Popconfirm
              title="Are you sure you want to delete this user?"
              onConfirm={() => confirmDeleteUser(id)}
              okText="Yes"
              cancelText="No"
            >
              <DeleteTwoTone style={{ fontSize: '20px' }} />
            </Popconfirm>
          </Tooltip>
        </div>
      ),
    },
  ]

  return (
    <div>
      {isLoading ? (
        <LoadingPage />
      ) : (
        <>
          {users && (
            <Table
              dataSource={users}
              columns={columns}
              pagination={false}
              rowKey={(user) => user.id}
              tableLayout={'fixed'}
              title={() => (
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <NewUserModal updateUsers={updateUsersList} />
                </div>
              )}
            />
          )}
        </>
      )}
    </div>
  )
}
