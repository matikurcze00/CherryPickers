import { Button, TextField, Grid, Container } from "@mui/material/";
import { Formik } from "formik";

export const LoginComponent = (props) => {
  if (props.logged) {
    return (
      <div>
        <Container maxWidth="sm">
          <Grid container>
            <Formik
              initialValues={{ email: "", password: "" }}
              validate={(values) => {
                const errors = {};
                if (!values.email) {
                  errors.email = "Required";
                } else if (
                  !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(values.email)
                ) {
                  errors.email = "Invalid email address";
                }
                return errors;
              }}
              onSubmit={(values, { setSubmitting }) => {
                setTimeout(() => {
                  alert(JSON.stringify(values, null, 2));
                  setSubmitting(false);
                }, 400);
              }}
            >
              {({
                values,
                errors,
                touched,
                handleChange,
                handleBlur,
                handleSubmit,
                isSubmitting,
                /* and other goodies */
              }) => (
                <form onSubmit={handleSubmit}>
                  <Grid margin={1} item>
                    <TextField
                      id="outlined-basic"
                      label="e-mail"
                      variant="outlined"
                      type="email"
                      name="email"
                      onChange={handleChange}
                      onBlur={handleBlur}
                      value={values.email}
                    />
                  </Grid>
                  {errors.email && touched.email && errors.email}
                  <Grid margin={1} item>
                    <TextField
                      id="outlined-basic"
                      label="password"
                      variant="outlined"
                      type="password"
                      name="password"
                      onChange={handleChange}
                      onBlur={handleBlur}
                      value={values.password}
                    />
                  </Grid>
                  {errors.password && touched.password && errors.password}
                  <Grid margin={1} item>
                    <Button
                      variant="outlined"
                      color="inherit"
                      type="submit"
                      disabled={isSubmitting}
                    >
                      SUBMIT
                    </Button>
                  </Grid>
                </form>
              )}
            </Formik>
          </Grid>
        </Container>
      </div>
    );
  }
};
