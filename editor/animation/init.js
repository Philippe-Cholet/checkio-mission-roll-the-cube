requirejs(['ext_editor_io', 'jquery_190'],
    function (extIO, $) {
        var $tryit;
        var io = new extIO({
            multipleArguments: true,
            functions: {
                python: 'roll_cube',
                // js: 'rollCube'
            }
        });
        io.start();
    }
);
