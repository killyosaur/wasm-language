 export enum Opcodes {
    end = 0x0b,
    get_local = 0x20,
    f32_add = 0x92
}

export enum Section {
    custom = 0,
    type,
    import,
    func,
    table,
    memory,
    global,
    export,
    start,
    element,
    code,
    data
}

export enum ExportType {
    func = 0x00,
    table = 0x01,
    mem = 0x02,
    global = 0x03
}

export enum Defaults {
    funcType = 0x60,
    emptyArr = 0x0
}

export enum ValType {
    i32 = 0x7f, // int 32
    f32 = 0x7d  // float 32
}