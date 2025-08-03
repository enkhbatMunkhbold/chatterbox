import { useNavigate } from "react-router-dom"


const NavBar = ({ user, setUser }) => {
  const navigate = useNavigate()

  const handleSignOut = () => {
    fetch('/logout', {
      method: 'DELETE',
      credentials: 'include',
    }).then(() => {
      setUser(null)
      navigate('/home')
    })
  }

  const handleLogin = () => {
    navigate('/signout')
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