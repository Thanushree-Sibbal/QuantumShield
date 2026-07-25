import { Card, CardContent, Typography } from "@mui/material";

export default function Timeline() {
  return (
    <Card
      sx={{
        background: "#151C32",
        color: "white",
        border: "1px solid #27314E",
        minHeight: 180,
      }}
    >
      <CardContent>
        <Typography variant="h6">Detection Timeline</Typography>
      </CardContent>
    </Card>
  );
}