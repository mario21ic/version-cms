<?php
include $argv[1]."/version.php";
echo json_encode(new JVersion);
