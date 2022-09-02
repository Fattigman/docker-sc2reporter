import React, { useEffect } from 'react'
import styles from './App.module.css'
import { Layout, Menu } from 'antd'
import { Link, Route, Routes, useLocation } from 'react-router-dom'
import { Samples } from './pages/Samples'
import { LoginPage } from './pages/Login/LoginPage'
import { getToken } from './services/api'

const { Header, Content } = Layout
export const App = () => {
  const [isLoading, setIsLoading] = React.useState<boolean>(true)
  const [user, setUser] = React.useState<any>()
  const [token, setToken] = React.useState<any>()
  const location = useLocation()

  const login = (formInput) => {
    getToken(formInput).then((response) => console.log(response))
  }

  return (
    <div className="app">
      <Layout style={{ minHeight: '100vh' }}>
        <Header className={styles.header}>
          <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={['home']}
            selectedKeys={[location.pathname]}
          >
            <Menu.Item key="/samples" disabled={!token}>
              <Link to="/samples">
                <span>Samples</span>
              </Link>
            </Menu.Item>
            {!!token && !!user?.username && (
              <Menu.Item key="/user" disabled={!token} style={{ marginLeft: 'auto' }}>
                {user?.username}
              </Menu.Item>
            )}
          </Menu>
        </Header>
        <Content
          className={styles.siteLayout}
          style={{
            padding: '0 50px',
            marginTop: 64,
            minHeight: 'calc(100vh - 155px)',
          }}
        >
          <Routes>
            <Route path="/" element={token ? <Samples /> : <LoginPage login={login} />} />
          </Routes>
        </Content>
        <footer data-testid="footer" className={styles.footer}>
          <a href={'https://www.scilifelab.se/units/clinical-genomics/'}>Clinical Genomics</a>
        </footer>
      </Layout>
    </div>
  )
}
