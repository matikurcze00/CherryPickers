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

function ButtonAppBar() {
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
            <Box>
              <Grid spacing={2} container>
                <Grid xs="9" item>
                  <Button disabled variant="outlined" color="secondary">
                    Export Configuration
                  </Button>
                </Grid>
                <Grid xs="3" item>
                  <Button variant="outlined" color="inherit">
                    Login
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
