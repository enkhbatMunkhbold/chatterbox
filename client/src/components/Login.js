import { useFormik } from 'formik'
import { useState } from 'react'
import { useHistory, Link } from 'react-router-dom'
import * as Yup from 'yup'
import '../styling/login.css'
import { apiCall } from '../config'

const Login = ({ user, setUser}) => {
  const [ error, setError ] = useState('')
  const history = useHistory()

  const formik = useFormik({
    initialValues: {
      username: "",
      password: ""
    },
    validationSchema: Yup.object({
      username: Yup.string().required("Username is required"),
      password: Yup.string().required("Password is required")
    }),
    onSubmit: (values) => {
      apiCall("/login", {
        method: "POST",
        body: JSON.stringify(values)
      })
      .then(res => {
        if(!res.ok) {
          return res.json().then(err => {
            throw new Error(err.message || "Invalid credentials")
          })
        }
        return res.json()
      })
      .then(user => {
        setUser(user)
        history.push("/home")
      })
      .catch(err => {
        setError(err.message || "Invalid credentials")
      })
    }
  })

  return (
    <div className='auth-container'>
      <form onSubmit={formik.handleSubmit} className='auth-form'>
        <h2>Login</h2>
        {error && <p className="error-message" style={{ color: "red" }}>{error}</p>}
        <div className='form-group'>
          <input
            type='text'
            name='username'
            placeholder='Username' 
            autoComplete='off'
            value={formik.values.username}
            onChange={formik.handleChange}
          />
          {formik.touched.username && formik.errors.username ? (
            <p className='error-message' style={{ color: "red" }}>{formik.errors.password}</p>
          ) : null}
        </div>
        <div className='form-group'>
          <input 
            type="password"
            name="password"
            placeholder='Password'
            value={formik.values.password}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            autoComplete='new-password'
          />
          {formik.touched.password && formik.errors.password && (
            <p style={{ color: "red" }}>{formik.errors.password}</p>
          )}
        </div>
        <button type="submit">Login</button>
        <div className='auth-link'>
          Don't have an account? <Link to="/register">Register</Link>
        </div>
      </form>
    </div>
  )
}

export default Login