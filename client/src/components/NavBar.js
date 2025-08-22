import { useHistory } from "react-router-dom"


const NavBar = ({ user, setUser }) => {
  const history = useHistory()

  const handleSignOut = () => {
    fetch('/logout', {
      method: 'DELETE',
      credentials: 'include',
    }).then(() => {
      setUser(null)
      history.push('/home')
    })
  }

  const handleLogin = () => {
    history.push('/login')
  }



  return (
    <nav className='navbar'>
      <h1>CHATBOX</h1>
        {user ? (
          <button className="nav-button signout-button" onClick={handleSignOut}>
            Sign Out
          </button>) : (
          <button className="nav-button login-button" onClick={handleLogin}>
            Login
          </button>
        )}
    </nav>
  )
}

export default NavBar