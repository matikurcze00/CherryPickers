import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import { Button, Grid } from "@mui/material";
import IconButton from "@mui/material/IconButton";
import MenuItem from "@mui/material/MenuItem";
import MenuIcon from "@mui/material/menu";
import icon from "../Logo_Ministerstwa_Finansów.svg.png";
import "./css/AppBar.css";
import { LoginComponent } from "./LoginComponent";
import {useState} from 'react'

function ButtonAppBar() {

  const [loggingIn, setLoggingIn] = useState(false);

  const onButtonClick = (e) =>
  {
    loggingIn ? e.target.color = 'error' : e.target.color = 'inherit';
    setLoggingIn(!loggingIn);
  }

  return (
    <div>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <img
              className="icon"
              style={{ marginRight: 10, marginBottom: 10, marginTop: 10 }}
              width={80}
              height={80}
              src={icon}
            ></img>
            <Typography
              variant="h3"
              textAlign="left"
              component="div"
              sx={{ flexGrow: 1 }}
            >
              SendHybrid
            </Typography>
              <LoginComponent logged={loggingIn}>
  
              </LoginComponent>
            <Box sx={{ flexGrow: 0.1 }}>
              <Grid spacing={2} container>
                <Grid xs="4" item>
                  <Button onClick={onButtonClick} variant="outlined" color="inherit">
                    Logging in
                  </Button>
                </Grid>
                <Grid xs="8" item>
                  <Button disabled variant="outlined" color="secondary">
                    Export Configuration
                  </Button>
                </Grid>
              </Grid>
            </Box>
          </Toolbar>
        </AppBar>
      </Box>
    </div>
  );
}

export default ButtonAppBar;
