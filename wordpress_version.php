<?php
include $argv[1]."/version.php";
class WVersion {
    public $RELEASE = $wp_version;
    public $DEV_LEVEL = $wp_db_version;
}
echo json_encode(new WVersion);
