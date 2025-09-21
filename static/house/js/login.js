$(document).ready(function () {
    // 注册表单验证，确保只初始化一次
    $("#registeform").bootstrapValidator({
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            name: {
                validators: {
                    notEmpty: {
                        message: '用户名不能为空!'
                    },
                    stringLength: {
                        min: 6,
                        max: 10,
                        message: '用户名长度6到10个字符！'
                    },
                    regexp: {
                        regexp: /^[a-zA-Z0-9_]+$/,
                        message: '用户名只能包含大写、小写、数字和下画线'
                    }
                }
            },
            password: {
                validators: {
                    notEmpty: {
                        message: '密码不能为空!'
                    },
                    stringLength: {
                        min: 6,
                        max: 16,
                        message: '密码长度6到15个字符！'
                    },
                    different: {
                        field: 'name',
                        message: '密码不能与用户名相同'
                    }
                }
            },
            confirmPassword: {
                validators: {
                    notEmpty: {
                        message: '确认密码不能为空!'
                    },
                    stringLength: {
                        min: 6,
                        max: 16,
                        message: '确认密码长度6到15个字符！'
                    },
                    different: {
                        field: 'name',
                        message: '确认密码不能与用户名相同'
                    },
                    identical: {
                        field: 'password',
                        message: '两次密码输入不一致'
                    }
                }
            },
            email: {
                validators: {
                    notEmpty: {
                        message: '邮箱不能为空!'
                    },
                    emailAddress: {
                        message: '无效的邮箱地址'
                    }
                }
            }
        }
    });

    // 在点击注册按钮时验证表单
    $("#registe-btn").on('click', function () {
        let validator = $("#registeform").data('bootstrapValidator');
        // 手动触发验证
        validator.validate();

        if (validator.isValid()) {
            // 发起AJAX请求
            $.ajax({
                type: 'post',
                url: '/register',
                data: $("#registeform").serialize(),
                dataType: 'json',
                success: function (res) {
                    if (res.code === 1) { // 注册成功
                        alert(res.msg); // 显示成功消息
                        location.href = '/user/' + res.data; // 跳转到用户页面
                    } else {
                        // 重置表单并清除验证状态
                        let validator = $("#registeform").data('bootstrapValidator');
                        if (validator) {
                            $("#registeform").data('bootstrapValidator').resetForm(true);
                        }
                        alert(res.msg); // 显示失败信息
                    }
                }
            });
        }
    });


    $("#loginform").bootstrapValidator({
        fields: {
            name: {
                validators: {
                    notEmpty: { // 非空校验
                        message: '用户名不能为空!'
                    }
                }
            },
            password: {
                validators: {
                    notEmpty: {
                        message: '密码不能为空!'
                    }
                }
            },
        }
    })

    // 登陆
    $("#login-btn").on('click', function () {
        let validator = $("#loginform").data('bootstrapValidator');
        validator.isValid() //手动触发验证
        if (validator.isValid()) {
            $.ajax({
                type: 'post',
                url: '/login',
                data: $("#loginform").serialize(),
                dataType: 'json',
                success: function (res) {
                    if (res.code == 1) {
                        alert(res.msg);
                        location.href = '/user/' + res.data;
                    }
                    else {
                        let validator = $("#loginform").data('bootstrapValidator');
                        if (validator) {
                            $("#loginform").data('bootstrapValidator').resetForm(true);
                        }
                        alert(res.msg);
                    }
                }
            })
        }
    })

    $("#logout").on('click', function () {
        let status = confirm('确认是否退出登陆?')
        if(status)
        {
            $.ajax({
                type: 'post',
                url: '/logout',
                dataType: 'json',
                success: function(res)
                {
                    if(res.code == 1)
                    {
                        alert(res.msg);
                        location.href = '/';
                    }
                    else
                    {
                        alert(res.msg);
                    }
                }
            })
        }
    })
});
